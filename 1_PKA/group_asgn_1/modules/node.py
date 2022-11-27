from .state import CongklakState


class CongklakNode:
    '''class for Congklak node in search algorithms
    '''
    def __init__(self, node_id: int, state: CongklakState, action: int,
        parent: int, depth: int):

        self.node_id = node_id
        self.state = state
        self.parent = parent
        self.depth = depth
        self.action = action # which action is taken to produce this state

    def __lt__(self, other):
        if self.depth == other.depth:
            return self.node_id < other.node_id
        return self.depth > other.depth

    def __repr__(self):
        text = ', '.join([
            f"Node {self.node_id}",
            f"parent {self.parent}",
            f"depth {self.depth}",
            f"action {self.action}"
        ])
        return text
