import numpy as np

from .state import CongklakState
from typing import List, Tuple
from game import Game


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

def maximize_diff_score_strategy(state: CongklakState) \
    -> List[Tuple[int, int, CongklakState]]:
    next_states = []
    for i, action_num in enumerate(state.valid_actions()):
        next_state = state.action(action_num)
        on_player = state.player
        total_play = 2
        while on_player != 1-state.player:
            game = Game(
                        policies=[maximize_house_strategy, maximize_house_strategy],
                        initial_state=next_state,
                        player=state.player,
                        max_total_visited_states=total_play
                    )
            game.play()
            on_player = game.final_state.player
            total_play+=1
        next_boards = game.final_state.board
        diff = next_boards[state.player, 0] - next_boards[1-state.player, 0]
        next_states.append((diff, action_num, next_state))
    return next_states