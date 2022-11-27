import numpy as np

from .state import CongklakState
from .node import CongklakNode


def play(player, policy, initial_state=None, print_every=100):
    if initial_state is None:
        initial_state = CongklakState(player=player, verbose=False)
    else:
        assert isinstance(initial_state, CongklakState)

    node = CongklakNode(node_id=0, state=initial_state, action=0, parent=0, depth=0)

    total_states, total_visited_states, id_counter = 1, 0, 0
    final_state, final_node, node_list = None, node, [node]
    stack = [node]

    while len(stack) != 0:
        node = stack.pop()
        total_visited_states += 1
        if total_visited_states % print_every == 0:
            print(f'> Observed {total_visited_states:,d} states')
            print('Last state:')
            print(node.state)
            print()

        if node.state.is_terminal():
            final_node = node
            final_state = node.state
            break

        next_states = sorted(policy(node.state))
        for priority_value, action_num, next_state in next_states:
            id_counter += 1
            total_states += 1
            next_node = CongklakNode(
                node_id=id_counter,
                state=next_state,
                parent=node.node_id,
                depth=node.depth + 1,
                action=action_num
            )
            node_list.append(next_node)
            stack.append(next_node)

    print('[RESULT]')
    print(f'> Total observed states: {total_visited_states}')
    print('> Final state:')
    print(final_state)

    player_beads = final_state.total_beads()
    if player_beads[0] != player_beads[1]:
        winner = np.argmax(player_beads)
        print(f'> Winner: player {winner} with {player_beads[winner]} beads!!')
        print(f'> Total steps to win: {final_node.depth}')
    else:
        print('> Game draw!!')
        print(f'> Total steps to draw: {final_node.depth}')

    return total_visited_states, final_node, node_list
