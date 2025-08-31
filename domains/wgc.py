from typing import Tuple, List, Any, Optional

State = Tuple[str, str, str, str]

class WGCProblem:
    def __init__(self, initial_state: State = ('0', '0', '0', '0')):
        self._initial_state = initial_state
        self._goal_state = ('1', '1', '1', '1')

    @property
    def initial_state(self) -> State:
        return self._initial_state

    def is_goal(self, state: State) -> bool:
        return state == self._goal_state

    def actions(self, state: State) -> List[str]:
        possible_actions = ['Move Goat', 'Move Wolf', 'Move Cabbage', 'Move Alone']
        valid_actions = []
        
        farmer_pos = state[0]
        
        if state[1] == farmer_pos:
            valid_actions.append('Move Wolf')
        if state[2] == farmer_pos:
            valid_actions.append('Move Goat')
        if state[3] == farmer_pos:
            valid_actions.append('Move Cabbage')
        valid_actions.append('Move Alone')

        return valid_actions

    def result(self, state: State, action: str) -> Optional[State]:
        farmer, wolf, goat, cabbage = state
        
        new_farmer_pos = '1' if farmer == '0' else '0'
        
        new_state_list = list(state)
        new_state_list[0] = new_farmer_pos

        if action == 'Move Wolf':
            new_state_list[1] = new_farmer_pos
        elif action == 'Move Goat':
            new_state_list[2] = new_farmer_pos
        elif action == 'Move Cabbage':
            new_state_list[3] = new_farmer_pos
        
        new_state = tuple(new_state_list)

        if self._is_valid(new_state):
            return new_state
        return None

    def step_cost(self, state: State, action: str) -> int:
        return 1

    def _is_valid(self, state: State) -> bool:
        farmer, wolf, goat, cabbage = state
        
        if wolf == goat and farmer != wolf:
            return False
            
        if goat == cabbage and farmer != goat:
            return False
            
        return True
