import numpy as np

from .state import CongklakState
from typing import List, Tuple
from .game import Game


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
        next_states.append(((-1 * house_beads, np.random.random()), action_num, next_state))
    return next_states


def get_max_diff(opp_strategy):
    def maximize_diff_score_strategy(state: CongklakState):
        next_states = []
        for i, action_num in enumerate(state.valid_actions()):
            next_state = state.action(action_num)
            if next_state.player == state.player:
                continue
            score_list = opp_strategy(next_state)
            score_list = sorted([x for x in score_list if x[2].player != state.player])
            next_next_state = score_list[0][2] if len(score_list) > 0 else next_state
            next_boards = next_next_state.board
            diff = next_boards[state.player, 0] - next_boards[1-state.player, 0]
            next_states.append(((-1*diff, np.random.random()), action_num, next_state))
        return next_states

    return maximize_diff_score_strategy