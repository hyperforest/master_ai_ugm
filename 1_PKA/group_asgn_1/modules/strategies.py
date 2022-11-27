import numpy as np

from .state import CongklakState
from typing import List, Tuple


def simple_strategy(state):
    next_states = []
    for i, action_num in enumerate(state.valid_actions()):
        next_states.append((i, action_num, state.action(action_num)))
    return next_states


def random_strategy(state: CongklakState):
    next_states = []
    for i, action_num in enumerate(state.valid_actions()):
        next_state = state.action(action_num)
        next_states.append((np.random.random(), action_num, next_state))
    return next_states


def maximize_house_strategy(state: CongklakState) \
    -> List[Tuple[int, int, CongklakState]]:

    next_states = []
    for i, action_num in enumerate(state.valid_actions()):
        next_state = state.action(action_num)
        house_beads = state.board[state.player, 0]
        next_states.append((-1 * house_beads, action_num, next_state))
    return next_states

def maximize_diff_score_strategy(state: CongklakState):
    pass