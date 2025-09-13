# File: run.py

import argparse
import sys
import os
from typing import List, Tuple, Any

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from search_core import Node, bfs, ids, astar
from table_generator import generate_combined_table_image
from domains.puzzle_generator import generate_puzzle

def format_wgc_path(node: Node) -> List[Tuple[Any, str, Any]]:
    path = []
    while node.parent:
        path.append((node.parent.state, node.action, node.state))
        node = node.parent
    path.reverse()
    return path

def print_8puzzle_state(state: Tuple[int, ...]):
    for i in range(0, 9, 3):
        row = state[i:i+3]
        print(" │ " + " ".join(str(x) if x != 0 else ' ' for x in row) + " │")

def main():
    parser = argparse.ArgumentParser(description="Run search algorithms on various domains.")
    parser.add_argument("domain", type=str, choices=["wgc", "8puzzle"], help="The problem domain to solve.")
    parser.add_argument("algorithm", type=str, nargs='?', default=None, help="The search algorithm to use for a single run.")
    parser.add_argument("initial_state", type=str, nargs='?', default=None, help="For 8-puzzle: the initial state as a comma-separated string.")
    
    parser.add_argument("--heuristic", type=str, choices=["h1", "h2"], help="For A* on 8-puzzle: h1 or h2.")
    parser.add_argument('--gentable', nargs='+', choices=['bfs', 'ids', 'ucs', 'astar_h1', 'astar_h2'], help='Generate a comparison table for the given algorithms.')
    
    parser.add_argument('--instances', type=int, default=1, help='Number of instances to run.')
    parser.add_argument('--randomstart', action='store_true', help='Generate random start state(s) for the 8-puzzle.')
    parser.add_argument('--shuffles', type=int, default=100, help='Number of random moves to generate a puzzle.')

    args = parser.parse_args()

    if args.domain == 'wgc' and (args.randomstart or args.instances > 1):
        parser.error("--randomstart and --instances > 1 are only supported for the 8puzzle domain.")
    if args.randomstart and args.initial_state:
        parser.error("Cannot specify an initial_state when using --randomstart.")

    initial_states = []
    if args.domain == '8puzzle':
        if args.randomstart:
            print(f"Generating {args.instances} random 8-puzzle instance(s)...")
            puzzles = set()
            while len(puzzles) < args.instances:
                puzzles.add(generate_puzzle(shuffles=args.shuffles))
            initial_states = list(puzzles)
        elif args.initial_state:
            try:
                initial_states.append(tuple(map(int, args.initial_state.split(','))))
            except (ValueError, TypeError):
                parser.error("Initial state for 8-puzzle must be 9 unique comma-separated integers.")
    elif args.domain == 'wgc':
        initial_states.append(('0','0','0','0'))

    all_instance_results = []
    algo_map = {
        'bfs': ('BFS', bfs, {}), 'ids': ('IDS', ids, {}),
        'ucs': ('UCS', astar, {'heuristic_variant': 'h0'}),
        'astar_h1': ('A* (h1)', astar, {'heuristic_variant': 'h1'}),
        'astar_h2': ('A* (h2)', astar, {'heuristic_variant': 'h2'})
    }

    algos_to_run = args.gentable if args.gentable else [args.algorithm]
    if algos_to_run == [None]:
        parser.error("You must specify an algorithm for a single run, or use --gentable.")

    for i, state in enumerate(initial_states):
        print(f"\n--- Running Instance {i+1}/{len(initial_states)} | Start State: {state} ---")
        
        if args.domain == 'wgc':
            from domains.wgc import WGCProblem
            problem = WGCProblem()
            domain_name = "WGC"
        else:
            from domains.eight_puzzle import EightPuzzleProblem
            problem = EightPuzzleProblem(state)
            domain_name = "8-Puzzle"

        instance_results_data = {}
        for algo_key in algos_to_run:
            if algo_key in ['ucs', 'astar_h1', 'astar_h2'] and args.domain != '8puzzle':
                print(f"Skipping {algo_key} for {args.domain} domain.")
                continue

            if args.gentable:
                 name, func, kwargs = algo_map[algo_key]
            else:
                name = args.algorithm.upper()
                func = {'bfs': bfs, 'ids': ids, 'astar': astar, 'ucs': astar}.get(args.algorithm)
                kwargs = {}
                if args.algorithm in ['astar', 'ucs']:
                    heuristic = 'h0' if args.algorithm == 'ucs' else args.heuristic
                    if args.algorithm == 'astar' and not heuristic: parser.error("A* requires --heuristic.")
                    kwargs = {'heuristic_variant': heuristic}
                    name = f"A* ({heuristic.upper()})" if args.algorithm == 'astar' else "UCS"
            
            print(f"  - Running {name}...")
            solution_node, metrics = func(problem, **kwargs)
            
            result_entry = {}
            if solution_node:
                result_entry.update({
                    "Solution Cost": solution_node.path_cost, "Solution Depth": solution_node.depth,
                    "Nodes Generated": metrics['nodes_generated'], "Nodes Expanded": metrics['nodes_expanded'],
                    "Max Frontier Size": metrics['max_frontier_size'],
                    "node": solution_node
                })
            else:
                result_entry.update({m: 'N/A' for m in ["Solution Cost", "Solution Depth"]})
                result_entry.update(metrics)
                result_entry['node'] = None
            instance_results_data[name] = result_entry

        all_instance_results.append({
            'initial_state': state,
            'domain': domain_name,
            'results_data': instance_results_data
        })

    if args.gentable:
        generate_combined_table_image(all_instance_results)
    else:
        for instance in all_instance_results:
            print(f"\n--- CONSOLE REPORT: Instance starting {instance['initial_state']} ---")
            for algo_name, results in instance['results_data'].items():
                print(f"\nDomain: {instance['domain']} | Algorithm: {algo_name}")
                solution_node = results['node']
                if solution_node:
                    print("-" * 25)
                    print("Solution Found!")
                    print(f"Solution cost: {results['Solution Cost']} | Depth: {results['Solution Depth']}")
                    print(f"Nodes generated: {results['Nodes Generated']} | Nodes expanded: {results['Nodes Expanded']} | Max frontier: {results['Max Frontier Size']}")
                    path = format_wgc_path(solution_node)
                    print("Path:")
                    if instance['domain'] == '8-Puzzle':
                        for i, (p_state, action, c_state) in enumerate(path, 1):
                            print(f"\nStep {i}: Action: {action}\nFrom:"); print_8puzzle_state(p_state); print("To:"); print_8puzzle_state(c_state)
                    else:
                        for i, (p_state, action, c_state) in enumerate(path, 1):
                            print(f"  {i}) {action:<15} {p_state} -> {c_state}")
                else:
                    print("\nNo solution found.")
                    print(f"Nodes generated: {results['nodes_generated']} | Nodes expanded: {results['nodes_expanded']} | Max frontier: {results['max_frontier_size']}")

if __name__ == "__main__":
    main()
