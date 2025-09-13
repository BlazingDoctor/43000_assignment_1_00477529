import random
from typing import Tuple, List

def generate_puzzle(shuffles: int = 100) -> Tuple[int, ...]:
    """
    Generates a solvable 8-puzzle by starting with the goal state
    and applying a number of random, valid moves.

    Args:
        shuffles (int): The number of random moves to apply.

    Returns:
        A tuple representing the shuffled, solvable puzzle state.
    """
    state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    
    for _ in range(shuffles):
        blank_index = state.index(0)
        row, col = divmod(blank_index, 3)
        
        valid_actions = []
        if row > 0: valid_actions.append('Up')
        if row < 2: valid_actions.append('Down')
        if col > 0: valid_actions.append('Left')
        if col < 2: valid_actions.append('Right')
        
        action = random.choice(valid_actions)
        
        swap_index = -1
        if action == 'Up':
            swap_index = blank_index - 3
        elif action == 'Down':
            swap_index = blank_index + 3
        elif action == 'Left':
            swap_index = blank_index - 1
        elif action == 'Right':
            swap_index = blank_index + 1
            
        state[blank_index], state[swap_index] = state[swap_index], state[blank_index]
        
    return tuple(state)