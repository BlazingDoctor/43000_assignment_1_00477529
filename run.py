import argparse
import sys
import os
from typing import List, Tuple, Any

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)
# -----------------------------

from domains.wgc import WGCProblem
from search_core import bfs, ids, Node

def format_path(node: Node) -> List[Tuple[Any, str]]:
    path = []
    while node.parent:
        path.append(((node.parent.state), node.action, node.state))
        node = node.parent
    path.reverse()
    return path

def main():
    parser = argparse.ArgumentParser(description="Run search algorithms on the WGC domain.")
    # Changed to a simple positional argument
    parser.add_argument("algorithm", type=str, choices=["bfs", "ids"], help="The search algorithm to use: 'bfs' or 'ids'.")
    args = parser.parse_args()

    # Domain is now hardcoded since we only have one
    problem = WGCProblem()
    domain_name = "WGC"
    
    search_function = None
    if args.algorithm == "bfs":
        search_function = bfs
    elif args.algorithm == "ids":
        search_function = ids

    solution_node, metrics = search_function(problem)

    print(f"Domain: {domain_name.upper()} | Algorithm: {args.algorithm.upper()}")

    if solution_node:
        print(f"Solution cost: {solution_node.path_cost} | Depth: {solution_node.depth}")
        print(f"Nodes generated: {metrics['nodes_generated']} | Nodes expanded: {metrics['nodes_expanded']} | Max frontier: {metrics['max_frontier_size']}")
        
        path = format_path(solution_node)
        print("Path:")
        for i, (parent_state, action, child_state) in enumerate(path, 1):
            action_name = action.replace("Move", "Move").replace("Alone", " alone")
            print(f"  {i}) {action_name:<15} {parent_state} -> {child_state}")
    else:
        print("No solution found.")
        print(f"Nodes generated: {metrics['nodes_generated']} | Nodes expanded: {metrics['nodes_expanded']} | Max frontier: {metrics['max_frontier_size']}")


if __name__ == "__main__":
    main()