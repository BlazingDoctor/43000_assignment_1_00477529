import collections
import heapq
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
    
def astar(problem, heuristic_variant: str) -> Tuple[Optional[Node], Dict[str, int]]:
    metrics = {
        "nodes_generated": 0,
        "nodes_expanded": 0,
        "max_frontier_size": 0,
    }
    
    counter = 0
    start_node = Node(problem.initial_state)
    h_start = problem.heuristic(start_node.state, heuristic_variant)
    f_start = start_node.path_cost + h_start
    
    frontier = [(f_start, counter, start_node)]
    counter += 1
    heapq.heapify(frontier)
    
    explored = {start_node.state: start_node.path_cost}
    
    metrics["nodes_generated"] += 1
    metrics["max_frontier_size"] = 1

    while frontier:
        _, _, node = heapq.heappop(frontier)
        if node.path_cost > explored[node.state]:
            continue
            
        metrics["nodes_expanded"] += 1

        if problem.is_goal(node.state):
            return node, metrics

        for action in problem.actions(node.state):
            child_state = problem.result(node.state, action)
            
            if child_state is None:
                continue

            g_cost_child = node.path_cost + problem.step_cost(node.state, action)

            if child_state not in explored or g_cost_child < explored[child_state]:
                explored[child_state] = g_cost_child
                
                h_cost_child = problem.heuristic(child_state, heuristic_variant)
                f_cost_child = g_cost_child + h_cost_child

                child_node = Node(
                    child_state,
                    node,
                    action,
                    g_cost_child
                )
                
                heapq.heappush(frontier, (f_cost_child, counter, child_node))
                counter += 1
                metrics["nodes_generated"] += 1
                metrics["max_frontier_size"] = max(metrics["max_frontier_size"], len(frontier))

    return None, metrics

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
