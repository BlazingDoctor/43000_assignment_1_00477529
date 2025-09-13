from typing import Tuple, List, Optional

State = Tuple[int, ...]
GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)

class EightPuzzleProblem:
    def __init__(self, initial_state: State):
        self._initial_state = initial_state
        self._goal_state = GOAL_STATE
        self._goal_positions = {val: i for i, val in enumerate(self._goal_state)}

    @property
    def initial_state(self) -> State:
        return self._initial_state

    def is_goal(self, state: State) -> bool:
        return state == self._goal_state

    def actions(self, state: State) -> List[str]:
        blank_index = state.index(0)
        row, col = divmod(blank_index, 3)
        valid_actions = []
        if row > 0: valid_actions.append('Move Up')
        if row < 2: valid_actions.append('Move Down')
        if col > 0: valid_actions.append('Move Left')
        if col < 2: valid_actions.append('Move Right')
        return valid_actions

    def result(self, state: State, action: str) -> State:
        blank_index = state.index(0)
        new_state_list = list(state)
        
        swap_index = -1
        if action == 'Move Up':
            swap_index = blank_index - 3
        elif action == 'Move Down':
            swap_index = blank_index + 3
        elif action == 'Move Left':
            swap_index = blank_index - 1
        elif action == 'Move Right':
            swap_index = blank_index + 1
        
        new_state_list[blank_index], new_state_list[swap_index] = new_state_list[swap_index], new_state_list[blank_index]
        return tuple(new_state_list)

    def step_cost(self, state: State, action: str) -> int:
        return 1
        
    def heuristic(self, state: State, variant: str) -> int:
        if variant == 'h0':
            return 0
        elif variant == 'h1':
            return self._h1_misplaced_tiles(state)
        elif variant == 'h2':
            return self._h2_manhattan_distance(state)
        else:
            raise ValueError(f"Unknown heuristic variant: {variant}")

    def _h1_misplaced_tiles(self, state: State) -> int:
        misplaced = 0
        for i in range(9):
            if state[i] != 0 and state[i] != self._goal_state[i]:
                misplaced += 1
        return misplaced

    def _h2_manhattan_distance(self, state: State) -> int:
        distance = 0
        for i in range(9):
            tile_value = state[i]
            if tile_value != 0:
                current_row, current_col = divmod(i, 3)
                goal_index = self._goal_positions[tile_value]
                goal_row, goal_col = divmod(goal_index, 3)
                distance += abs(current_row - goal_row) + abs(current_col - goal_col)
        return distance