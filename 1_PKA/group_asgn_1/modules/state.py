import numpy as np
# from .strategies import maximize_house_strategy, get_max_diff

class CongklakState:
    '''class for Congklak state
    '''

    def __init__(self, player: int = 0, board=None, holes: int = 7,
        init_beads: int = 7, verbose=False):

        self.player = player
        self.holes = holes
        self.init_beads = init_beads
        self.verbose = verbose

        if board is None:
            self.board = np.ones((2, holes + 1), dtype=np.int32) * init_beads
            self.board[:, 0] = 0
        elif isinstance(board, np.ndarray):
            assert board.ndim == 2
            self.board = board
            self.holes = board.shape[1] - 1


    def __repr__(self):
        return f"Player: {self.player}, board:\n{self.board}"


    def is_terminal(self):
        is_all_holes_empty = np.all(self.board[:, 1:] == 0)
        return is_all_holes_empty


    def is_able_to_move(self):
        return len(self.valid_actions()) > 0


    def is_valid_action(self, hole):
        return 0 < hole <= self.holes and self.board[self.player, hole] > 0


    def valid_actions(self):
        return [x for x in range(1, self.holes + 1) if self.is_valid_action(x)]


    def total_beads(self):
        return self.board.sum(axis=1) 


    def _next(self, hole, lane):
        hole += 1
        if hole > self.holes:
            hole = 0
            lane = 1 - lane
        return hole, lane


    def _print(self, text, board=None):
        if self.verbose:
            if board is not None:
                print('> Board result:')
                print(board)
            print(text)

    # def auto(self, strategies):
    #     if (strategies == 'max_diff'):
    #         maximize_diff_score_strategy = get_max_diff(maximize_house_strategy)
    #         next_state = sorted(maximize_diff_score_strategy(self))[0][2]
    #         return next_state

    #     elif (strategies == 'max_house'):
    #         next_state = sorted(maximize_house_strategy(self))[0][2]
    #         return next_state

    def action(self, hole):
        assert(self.is_valid_action(hole))

        if not self.is_able_to_move():
            return CongklakState(
                player=1 - self.player,
                board=self.board,
                holes=self.holes,
                init_beads=self.init_beads,
                verbose=self.verbose
            )

        new_state = CongklakState(
            player=1 - self.player,
            board=self.board.copy(),
            holes=self.holes,
            init_beads=self.init_beads,
            verbose=self.verbose,
        )

        beads = new_state.board[self.player, hole]
        new_state.board[self.player, hole] = 0

        lane = self.player
        can_move = True
        self._print(f'> Start action {hole}, beads: {beads}')

        while can_move:
            assert beads >= 0
            hole, lane = self._next(hole, lane)

            if hole == 0: # stopped in any house
                if lane == self.player:
                    # stopped in own house
                    new_state.board[lane, hole] += 1
                    beads -= 1

                    text = f'Rem. beads: {beads}, have put into own house'
                    self._print(text, new_state.board)
                else:
                    # stopped in opp house
                    hole = 1

                    text = f'Rem. beads: {beads}, stopped in opp house'
                    self._print(text, new_state.board)

            if hole >= 1:
                new_state.board[lane, hole] += 1
                beads -= 1
                if lane == self.player:
                    text = f'Rem. beads: {beads}, have put into own hole {hole}'
                else:
                    text = f'Rem. beads: {beads}, have put into opp hole {hole}'

                self._print(text, new_state.board)

            if beads == 0:
                if hole == 0:
                    text = 'Stopped in own house! Bonus move!'
                    self._print(text, new_state.board)
                    new_state.player = self.player
                    can_move = False
                else:
                    if lane == self.player:
                        text = f'Rem. beads: {beads}, stopped in own hole {hole}'
                    else:
                        text = f'Rem. beads: {beads}, stopped in opp hole {hole}'
                    self._print(text, new_state.board)

                    if new_state.board[lane, hole] > 1: # not empty
                        # can move again
                        new_state.player = self.player
                        can_move = True

                        # take all beads in hole
                        beads = new_state.board[lane, hole]
                        new_state.board[lane, hole] = 0
                    else:
                        new_state.player = 1 - self.player
                        can_move = False
                        
                        if lane == self.player:
                            # take all beads in opp hole
                            beads = new_state.board[1 - lane, hole]
                            new_state.board[1 - lane, hole] = 0

                            # take all beads in own hole
                            beads += new_state.board[lane, hole]
                            new_state.board[lane, hole] = 0

                            # put in own house
                            new_state.board[self.player, 0] += beads

                            text = f'Bonus {beads} beads!! (end turn)'
                            self._print(text, new_state.board)

        self._print('[Action stopped]')
        return new_state
