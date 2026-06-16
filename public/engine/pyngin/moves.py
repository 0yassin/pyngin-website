from pyngin.pieces import PST_PAWN, PST_KNIGHT, PST_BISHOP, PST_ROOK, PST_QUEEN

def get_move_score(move, board):
    start, end = move
    moving_piece = abs(board.state[start])
    victim_piece = abs(board.state[end])
    score = 0
    if victim_piece != 0:
        score = (9999) + (victim_piece * 10) - moving_piece
        return score
    if moving_piece == 1:
        if (end >> 3) == 0 or (end >> 3) == 7:
            score += 9999
    piece_color = 1 if board.state[start] > 0 else -1
    pst_index = end if piece_color > 0 else (end ^ 56)
    if moving_piece == 1:
        score += PST_PAWN[pst_index] * 2
    elif moving_piece == 2:
        score += PST_KNIGHT[pst_index] * 2
    elif moving_piece == 3:
        score += PST_BISHOP[pst_index] * 2
    elif moving_piece == 4:
        score += PST_ROOK[pst_index] * 2
    elif moving_piece == 5:
        score += PST_QUEEN[pst_index] * 2
    # TODO: add king move bonuses
    return score

def get_knight_moves(board, index, res):
    st_row, st_col = index >> 3, index & 7
    deltas = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
    is_white = board.state[index] > 0
    for dr, dc in deltas:
        r, c = st_row + dr, st_col + dc
        if 0 <= r < 8 and 0 <= c < 8:
            tar_square = (r << 3) + c
            piece = board.state[tar_square]
            if piece == 0 or (piece > 0) != is_white:
                res.append((index, tar_square))

def get_sliding_moves(board, index, deltas , res):
    st_row, st_col = index >> 3, index & 7
    is_white = board.state[index] > 0
    for dr, dc in deltas:
        r, c = st_row + dr, st_col + dc
        while 0 <= r < 8 and 0 <= c < 8:
            tar_square = (r << 3) + c
            piece = board.state[tar_square]
            if piece == 0:
                res.append((index, tar_square))
            elif (piece > 0) == is_white: 
                break
            else:
                res.append((index, tar_square))
                break
            r += dr
            c += dc

def get_bishop_moves(board, index, res):
     get_sliding_moves(board, index, [(-1,-1), (-1,1), (1,-1), (1,1)], res)

def get_rook_moves(board, index, res):
    get_sliding_moves(board, index, [(-1,0), (1,0), (0,-1), (0,1)], res)

def get_pawn_moves(board, index, res):
    is_white = board.state[index] > 0
    st_row, st_col = index >> 3, index & 7
    direction = -1 if is_white else 1
    next_row = st_row + direction
    if 0 <= next_row < 8:
        tar_square = (next_row << 3) + st_col
        if board.state[tar_square] == 0:
            res.append((index, tar_square))
            if (st_row == 6 and is_white) or (st_row == 1 and not is_white):
                double_square = ((st_row + (direction << 1)) << 3) + st_col
                if board.state[double_square] == 0:
                    res.append((index, double_square))
        for dc in [-1, 1]:
                c = st_col + dc
                if 0 <= c < 8:
                    tar_square = (next_row << 3) + c
                    piece = board.state[tar_square]
                    if piece != 0 and (piece > 0) != is_white:
                        res.append((index, tar_square))
                    elif board.en_passant_target is not None and tar_square == board.en_passant_target:
                        res.append((index, tar_square))

def get_queen_moves(board, index, res):
     get_sliding_moves(board, index, [(-1,-1), (-1,1), (1,-1), (1,1), (-1,0), (1,0), (0,-1), (0,1)], res)

def get_king_moves(board, index, res):
    st_row, st_col = index >> 3, index & 7
    is_white = board.state[index] > 0
    if board.turn == "w" and index == 60:
        if (board.castling_rights & 1) and board.state[61] == 0 and board.state[62] == 0:
            res.append((60, 62))
        if (board.castling_rights & 2) and board.state[59] == 0 and board.state[58] == 0 and board.state[57] == 0:
            res.append((60, 58))
    elif board.turn == "b" and index == 4:
        if (board.castling_rights & 4) and board.state[5] == 0 and board.state[6] == 0:
            res.append((4, 6))
        if (board.castling_rights & 8) and board.state[3] == 0 and board.state[2] == 0 and board.state[1] == 0:
            res.append((4, 2))

    deltas = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for dr, dc in deltas:
        r, c = st_row + dr, st_col + dc
        if 0 <= r < 8 and 0 <= c < 8:
            tar_square = (r << 3) + c
            piece = board.state[tar_square]
            if piece == 0 or (piece > 0) != is_white:
                res.append((index, tar_square))

def get_psudo_moves(board):
    p_moves = []
    is_white_turn = (board.turn == "w")
    for i, piece in enumerate(board.state):
        if piece == 0 or (piece > 0) != is_white_turn:
            continue
        match abs(piece):
            case 1: get_pawn_moves(board, i, p_moves)
            case 2: get_knight_moves(board, i, p_moves)
            case 3: get_bishop_moves(board, i, p_moves)
            case 4: get_rook_moves(board, i, p_moves)
            case 5: get_queen_moves(board, i, p_moves)
            case 6: get_king_moves(board, i, p_moves)
    return p_moves

def get_legal_moves(board):
    legal_moves = []
    pseudo_moves = get_psudo_moves(board)
    king_index = board.bk_index if board.turn == "b" else board.wk_index
    opponent_color = 'b' if board.turn == 'w' else 'w'
    ep_captured_piece = 0
    for move in pseudo_moves:
        start, end = move
        piece_moving = board.state[start]
        captured_piece = board.state[end]
        is_castling_move = (abs(piece_moving) == 6 and abs(start - end) == 2)
        is_king_moving = (abs(piece_moving) == 6)
        board.state[end] = piece_moving
        board.state[start] = 0
        ep_victim_square = None
        if abs(piece_moving) == 1 and ((start & 7) != (end & 7) and captured_piece == 0):
            ep_victim_square = end + 8 if piece_moving > 0 else end - 8
            ep_captured_piece = board.state[ep_victim_square]
            board.state[ep_victim_square] = 0
        temp_king_idx = end if is_king_moving else king_index
        king_is_safe = not is_square_attacked(temp_king_idx, board, opponent_color)
        if king_is_safe and is_castling_move:
            transit_square = (start + end) >> 1
            if is_square_attacked(start, board, opponent_color) or \
               is_square_attacked(transit_square, board, opponent_color):
                king_is_safe = False
        if king_is_safe:
            legal_moves.append(move)
        board.state[start] = piece_moving
        board.state[end] = captured_piece
        if ep_victim_square is not None:
            board.state[ep_victim_square] = ep_captured_piece
    return legal_moves

def is_square_attacked(square, board, opp_color):
    start_row, start_col = square >> 3, square & 7
    is_opp_white = (opp_color == "w")
    kn_deltas = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
    target_knight = 2 if is_opp_white else -2
    for dr, dc in kn_deltas:
        r, c = start_row + dr, start_col + dc
        if 0 <= r < 8 and 0 <= c < 8: 
            if board.state[(r << 3) + c] == target_knight:
                return True
    target_pawn = 1 if is_opp_white else -1
    p_row_delta = 1 if is_opp_white else -1
    for p_col_delta in [-1, 1]:
        r, c = start_row + p_row_delta, start_col + p_col_delta
        if 0 <= r < 8 and 0 <= c < 8:
            if board.state[(r << 3) + c] == target_pawn:
                return True
    target_rook = 4 if is_opp_white else -4
    target_queen = 5 if is_opp_white else -5
    ortho_deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in ortho_deltas:
        r, c = start_row + dr, start_col + dc
        while 0 <= r < 8 and 0 <= c < 8:
            piece = board.state[(r << 3) + c]
            if piece != 0:
                if piece == target_rook or piece == target_queen:
                    return True
                break  
            r += dr
            c += dc
    target_bishop = 3 if is_opp_white else -3
    diag_deltas = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    for dr, dc in diag_deltas:
        r, c = start_row + dr, start_col + dc
        while 0 <= r < 8 and 0 <= c < 8:
            piece = board.state[(r << 3) + c]
            if piece != 0:
                if piece == target_bishop or piece == target_queen:
                    return True
                break  # Ray is blocked
            r += dr
            c += dc
    target_king = 6 if is_opp_white else -6
    king_deltas = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for dr, dc in king_deltas:
        r, c = start_row + dr, start_col + dc
        if 0 <= r < 8 and 0 <= c < 8:
            if board.state[(r << 3) + c] == target_king:
                return True
    return False

def is_current_turn_piece(piece, turn):
    # piece > 0 means white
    if piece > 0 and turn == "w":
        return True
    elif piece < 0 and turn == "b":
        return True
    else:
        return False

def count_vision_squares(piece_index, board, offsets):
    count = 0
    for offset in offsets:
        tar_square = piece_index
        prev_col = piece_index & 7
        while True:
            tar_square += offset
            tar_col = tar_square & 7
            if tar_square > 63 or tar_square < 0:
                break
            elif offset in [-8, 8] and tar_col != prev_col:
                break  
            elif offset in [-9, -7, 9, 7, 1, -1] and abs(tar_col - prev_col) != 1:
                break
            count += 1
            if board.state[tar_square] != 0:
                break
            prev_col = tar_col
    return count

def translate_move(move):
    st_row, end_row = move[0] >> 3, move[1] >> 3
    st_col, end_col = move[0] & 7, move[1] & 7
    st_file = chr(97 + st_col)
    st_rank = str(8 - st_row)
    end_file = chr(97 + end_col)
    end_rank = str(8 - end_row)
    return st_file + st_rank + end_file + end_rank