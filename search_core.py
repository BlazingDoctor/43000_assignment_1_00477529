import collections
from typing import Any, Dict, Optional, Tuple, List

class Node:
    def __init__(self, state: Any, parent: Optional['Node'] = None, action: Optional[str] = None, path_cost: int = 0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self) -> str:
        return f"<Node {self.state}>"

    def expand(self, problem) -> List['Node']:
        return [
            self.child_node(problem, action)
            for action in problem.actions(self.state)
        ]

    def child_node(self, problem, action: str) -> Optional['Node']:
        next_state = problem.result(self.state, action)
        if next_state is None:
            return None
            
        return Node(
            next_state, 
            self, 
            action,
            self.path_cost + problem.step_cost(self.state, action)
        )

def bfs(problem) -> Tuple[Optional[Node], Dict[str, int]]:
    metrics = {
        "nodes_generated": 0,
        "nodes_expanded": 0,
        "max_frontier_size": 0,
    }
    
    start_node = Node(problem.initial_state)
    metrics["nodes_generated"] += 1
    
    if problem.is_goal(start_node.state):
        return start_node, metrics

    frontier = collections.deque([start_node])
    explored = {start_node.state}
    metrics["max_frontier_size"] = 1

    while frontier:
        node = frontier.popleft()
        metrics["nodes_expanded"] += 1

        for action in problem.actions(node.state):
            child_state = problem.result(node.state, action)
            
            if child_state is None or child_state in explored:
                continue

            metrics["nodes_generated"] += 1
            child_node = Node(
                child_state,
                node,
                action,
                node.path_cost + problem.step_cost(node.state, action)
            )

            if problem.is_goal(child_node.state):
                return child_node, metrics
            
            explored.add(child_state)
            frontier.append(child_node)
            metrics["max_frontier_size"] = max(metrics["max_frontier_size"], len(frontier))
    
    return None, metrics

def ids(problem) -> Tuple[Optional[Node], Dict[str, int]]:
    total_metrics = {
        "nodes_generated": 0,
        "nodes_expanded": 0,
        "max_frontier_size": 0,
    }
    
    for depth_limit in range(100):
        result, metrics = dls(problem, depth_limit)
        
        total_metrics["nodes_generated"] += metrics["nodes_generated"]
        total_metrics["nodes_expanded"] += metrics["nodes_expanded"]
        total_metrics["max_frontier_size"] = max(total_metrics["max_frontier_size"], metrics["max_frontier_size"])

        if result is not None:
            return result, total_metrics
            
    return None, total_metrics

def dls(problem, limit: int) -> Tuple[Optional[Node], Dict[str, int]]:
    metrics = {
        "nodes_generated": 1,
        "nodes_expanded": 0,
        "max_frontier_size": 1,
    }
    
    start_node = Node(problem.initial_state)
    frontier = [start_node]
    explored = {start_node.state: 0}

    while frontier:
        node = frontier.pop()
        metrics["nodes_expanded"] += 1

        if problem.is_goal(node.state):
            return node, metrics

        if node.depth >= limit:
            continue

        for action in problem.actions(node.state):
            child_state = problem.result(node.state, action)

            if child_state is None:
                continue
                
            child_node = Node(
                child_state,
                node,
                action,
                node.path_cost + problem.step_cost(node.state, action)
            )
            
            if child_state in explored and explored[child_state] <= child_node.depth:
                continue
            
            metrics["nodes_generated"] += 1
            explored[child_state] = child_node.depth
            frontier.append(child_node)
            metrics["max_frontier_size"] = max(metrics["max_frontier_size"], len(frontier))
    
    return None, metrics