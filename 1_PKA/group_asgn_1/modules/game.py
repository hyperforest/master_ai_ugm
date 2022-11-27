import numpy as np

from .state import CongklakState
from .node import CongklakNode


class Game:
    def __init__(self, policies, initial_state=None, print_every=100, player=0,
        verbose=True, max_total_visited_states=None):

        if initial_state is None:
            initial_state = CongklakState(player=player, verbose=False)
        else:
            assert isinstance(initial_state, CongklakState)
        
        self.policies = policies
        self.initial_state = initial_state
        self.print_every = print_every
        self.total_states = 0
        self.total_visited_states = 0
        self.id_counter = 0
        self.max_total_visited_states = max_total_visited_states
        self.verbose = verbose


    def _print(self, *args):
        if self.verbose:
            print(*args)


    def play(self):
        node = CongklakNode(
            node_id=0,
            state=self.initial_state,
            action=0,
            parent=0,
            depth=0
        )

        self.final_state = None
        self.final_node = node
        self.node_list = [node]
    
        stack = [node]
        while len(stack) != 0:
            node = stack.pop()
            self.total_visited_states += 1

            if self.max_total_visited_states is not None:
                if self.total_visited_states > self.max_total_visited_states:
                    self.final_node = node
                    self.final_state = node.state
                    break

            if self.total_visited_states % self.print_every == 0:
                text = f'> Observed {self.total_visited_states:,d} states'
                self._print(text)
                self._print('Last state:')
                self._print(node.state)
                self._print()

            if node.state.is_terminal():
                self.final_node = node
                self.final_state = node.state
                break

            next_states = self.policies[node.state.player](node.state)
            next_states = sorted(next_states, reverse=True)

            for priority_value, action_num, next_state in next_states:
                self.id_counter += 1
                self.total_states += 1
                next_node = CongklakNode(
                    node_id=self.id_counter,
                    state=next_state,
                    parent=node.node_id,
                    depth=node.depth + 1,
                    action=action_num
                )
                self.node_list.append(next_node)
                stack.append(next_node)

        self._print('[RESULT]')
        text = f'> Total observed states: {self.total_visited_states}'
        self._print(text)
        
        self._print('> Final state:')
        self._print(self.final_state)

        player_beads = self.final_state.total_beads()
        if player_beads[0] != player_beads[1]:
            winner = np.argmax(player_beads)
            text = f'> Winner: player {winner} with {player_beads[winner]} beads!!'
            print(text)

            text = f'> Total steps to win: {self.final_node.depth}'
            print(text)
        else:
            self._print('> Game draw!!')
            text = f'> Total steps to draw: {self.final_node.depth}'
            self._print(text)
