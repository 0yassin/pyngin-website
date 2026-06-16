from pyngin.pieces import *
from pyngin.moves import count_vision_squares

def evaluate_position(board):
    phase = 0
    mg_score = 0
    eg_score = 0

    white_pieces_count = 0
    black_pieces_count = 0
    white_king_idx = -1
    black_king_idx = -1
    for i in range(64):
        piece = board.state[i]
        if piece == 0: 
            continue
        if piece > 0:  
            white_pieces_count += 1
            if abs(piece) == 6: white_king_idx = i
        else:          
            black_pieces_count += 1
            if abs(piece) == 6: black_king_idx = i

    for i in range(64):
        piece = board.state[i]
        if piece == 0:
            continue
        piece_color = 1 if piece > 0 else -1
        pst_index = i if piece_color>0 else (i ^ 56)
        # material
        mg_score += PIECE_VALUES[abs(piece)] * piece_color
        eg_score += PIECE_VALUES[abs(piece)] * piece_color
        
        if abs(piece) == 2 or abs(piece) == 3:   phase += 1 
        elif abs(piece) == 4:                    phase += 2  
        elif abs(piece) == 5:                    phase += 4

        if abs(piece) == 1:
            mg_score += PST_PAWN[pst_index] * piece_color
            eg_score += (PST_PAWN[pst_index] * PAWN_EG_BONUS) * piece_color

        elif abs(piece) == 2:
            mg_score += PST_KNIGHT[pst_index] * piece_color
            eg_score += (PST_KNIGHT[pst_index] * KNIGHT_EG_BONUS) * piece_color 

        elif abs(piece) == 3:
            sq = count_vision_squares(i, board, BISHOP_OFFSETS)
            PST_score = PST_BISHOP[pst_index]
            b_score = (sq * BISHOP_VISION_BONUS) + PST_score
            mg_score += b_score * piece_color
            eg_score += b_score * piece_color

        elif abs(piece) == 4:
            sq = count_vision_squares(i, board, ROOK_OFFSETS)
            PST_score = PST_ROOK[pst_index]
            b_score = (sq * ROOK_VISION_BONUS) + PST_score
            mg_score += b_score * piece_color
            eg_score += b_score * piece_color

        elif abs(piece) == 5:
            sq = count_vision_squares(i, board, QUEEN_OFFSETS)
            PST_score = PST_QUEEN[pst_index]
            b_score = (sq * QUEEN_VISION_BONUS) + PST_score
            mg_score += b_score * piece_color
            eg_score += b_score * piece_color

        elif abs(piece) == 6:
            mg_score += PST_KING_MG[pst_index] * piece_color
            eg_score += PST_KING_EG[pst_index] * piece_color

    if black_pieces_count == 1 and white_pieces_count > 1:
        mg_score += calculate_mop_up(winner_king=white_king_idx, loser_king=black_king_idx) * 20
        eg_score += calculate_mop_up(winner_king=white_king_idx, loser_king=black_king_idx) * 20
        
    elif white_pieces_count == 1 and black_pieces_count > 1:
        mg_score -= calculate_mop_up(winner_king=black_king_idx, loser_king=white_king_idx) * 20
        eg_score -= calculate_mop_up(winner_king=black_king_idx, loser_king=white_king_idx) * 20

    phase = min(phase, 24)
    final_score = ((mg_score * phase) + (eg_score * (24 - phase))) // 24
    return int(final_score)

def get_relative_eval(board):
    eval = evaluate_position(board)
    return eval if board.turn == "w" else eval * -1


def calculate_mop_up(winner_king, loser_king):
    bonus = 0
    lk_row, lk_col = loser_king // 8, loser_king % 8
    wk_row, wk_col = winner_king // 8, winner_king % 8

    dist_center_row = max(3 - lk_row, lk_row - 4)
    dist_center_col = max(3 - lk_col, lk_col - 4)
    bonus += (dist_center_row + dist_center_col) * 10

    king_distance = abs(wk_row - lk_row) + abs(wk_col - lk_col)
    bonus += (14 - king_distance) * 4

    return bonus