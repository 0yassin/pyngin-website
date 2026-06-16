from pyngin.moves import translate_move, is_square_attacked, get_legal_moves
from chess import Move

CASTLING_MASKS = [15] * 64
CASTLING_MASKS[60] = 12
CASTLING_MASKS[63] = 14
CASTLING_MASKS[56] = 13
CASTLING_MASKS[4] = 3
CASTLING_MASKS[7] = 11
CASTLING_MASKS[0]  = 7

class Board:
    def __init__(self, state=None):
        if state is None:
            self.state:list[int] = [0]*64
            self.bk_index = 4
            self.wk_index = 60
        else:
            self.state = list(state)
            self.bk_index = self.state.index(-6)
            self.wk_index = self.state.index(6)

        self.castling_rights = 15
        self.en_passant_target = None
        self.move_n = 1
        self.turn = 'w'
        self.game_state = "-"
        self.pgn_node = None

    def get_possible_moves(self):
        return get_legal_moves(self)
        
    def make_move(self,move, pgn_game = None):
        start, end = move
        piece_moving = self.state[start]
        captured_piece = self.state[end]

        saved_state = (
            piece_moving,
            captured_piece,
            self.castling_rights,
            self.en_passant_target,
            self.wk_index,
            self.bk_index
        )

        next_ep_target = None

        if self.pgn_node is not None:
            chess_move = Move.from_uci(translate_move(move))
            self.pgn_node = self.pgn_node.add_main_variation(chess_move)

        if piece_moving == 6:
            self.wk_index = end
        elif piece_moving == -6:
            self.bk_index = end

        if abs(piece_moving) == 6:
            if start == 60 and end == 62:
                self.state[61] = self.state[63]
                self.state[63] = 0
            elif start == 60 and end == 58:
                self.state[59] = self.state[56]
                self.state[56] = 0
            elif start == 4 and end == 6:
                self.state[5] = self.state[7]
                self.state[7] = 0
            elif start == 4 and end == 2:
                self.state[3] = self.state[0]
                self.state[0] = 0

        self.castling_rights &= CASTLING_MASKS[start] & CASTLING_MASKS[end]

        if abs(piece_moving) == 1:
            start_row = start >> 3
            end_row = end >> 3
            if abs(end_row - start_row) == 2:
                next_ep_target = (start + end) >> 1
  
        if abs(piece_moving) == 1 and end == self.en_passant_target:
            victim_square = end + 8 if piece_moving > 0 else end - 8
            self.state[victim_square] = 0

        if abs(piece_moving) == 1:
            end_row = end >> 3
            if end_row == 0 or end_row == 7:
                self.state[end] = 5 if piece_moving > 0 else -5
            else:
                self.state[end] = piece_moving
        else:
            self.state[end] = piece_moving

        if pgn_game != None:
            pgn_game.add_main_variation(Move.from_uci(translate_move(move)))

        self.state[start] = 0
        self.en_passant_target = next_ep_target
        self.move_n += 1 if self.turn == "b" else 0
        self.turn = "b" if self.turn == "w" else "w"

        return saved_state

    def unmake_move(self, move, saved_state):
        start, end = move
        piece_moving, captured_piece, old_castling, old_ep, old_wk, old_bk = saved_state
        self.turn = "w" if self.turn == "b" else "b"
        self.move_n -= 1 if self.turn == "b" else 0
        self.en_passant_target = old_ep
        self.wk_index = old_wk
        self.bk_index = old_bk
        self.castling_rights = old_castling
        if abs(piece_moving) == 6 and abs(start - end) == 2:
            if start == 60 and end == 62:
                self.state[63] = self.state[61]
                self.state[61] = 0
            elif start == 60 and end == 58:
                self.state[56] = self.state[59]
                self.state[59] = 0
            elif start == 4 and end == 6:
                self.state[7] = self.state[5]
                self.state[5] = 0
            elif start == 4 and end == 2:
                self.state[0] = self.state[3]
                self.state[3] = 0
        if abs(piece_moving) == 1 and end == old_ep:
            victim_square = end + 8 if piece_moving > 0 else end - 8
            self.state[victim_square] = -1 if piece_moving > 0 else 1
        self.state[start] = piece_moving
        self.state[end] = captured_piece

    def clone(self):
        new_board = Board()
        new_board.state = list(self.state)
        new_board.castling_rights = self.castling_rights
        new_board.en_passant_target = self.en_passant_target
        new_board.move_n = self.move_n
        new_board.turn = self.turn
        new_board.wk_index = self.wk_index
        new_board.bk_index = self.bk_index
        return new_board

    def is_in_check(self):
        king_idx = self.wk_index if self.turn == 'w' else self.bk_index
        opp_color = 'b' if self.turn == 'w' else 'w'
        return is_square_attacked(king_idx, self, opp_color)