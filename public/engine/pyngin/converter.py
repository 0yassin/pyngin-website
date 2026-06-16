piece_table = {
    "p":-1, "r":-4, "n":-2, "b":-3, "q":-5, "k":-6,
    "P":1, "R":4, "N":2, "B":3, "Q":5, "K":6,
}

def load_fen(fen: str, board):
    parts = fen.split(" ")
    

    while len(parts) < 6:
        if len(parts) < 3: parts.append("-")
        if len(parts) < 4 : parts.append("-")
        if len(parts) < 5: parts.append("0")
        if len(parts) < 6: parts.append("1")
        else: raise ValueError("Malformed FEN string: too few parts.")


    ranks = parts[0].split("/")
    curr_square = 0
    for rank in ranks:
        for char in rank:
            if char in piece_table:
                board.state[curr_square] = piece_table[char]
                if piece_table[char] == 6: board.wk_index = curr_square
                elif piece_table[char] == -6: board.bk_index = curr_square
                curr_square += 1
            elif char.isdigit():
                empty_squares = int(char)
                for _ in range(empty_squares):
                    board.state[curr_square] = 0
                    curr_square += 1
            else:
                raise ValueError(f"Invalid character '{char}' in FEN placement data.")


    board.turn = parts[1].lower() 

    castling_str = parts[2]
    mask = 0
    if 'K' in castling_str: mask |= 1  # White King-side
    if 'Q' in castling_str: mask |= 2  # White Queen-side
    if 'k' in castling_str: mask |= 4  # Black King-side
    if 'q' in castling_str: mask |= 8  # Black Queen-side

    board.castling_rights = mask


    
    if parts[3] != "-":
        file_char = parts[3][0].lower()
        rank_char = parts[3][1]
        col = ord(file_char) - ord('a')
        row = 8 - int(rank_char)
        board.en_passant_target = (row * 8) + col
    else:
        board.en_passant_target = None

    try:
        board.halfmove_clock = int(parts[4])
    except ValueError:
        board.halfmove_clock = 0

    try:
        board.move_n = int(parts[5])
    except ValueError:
        board.move_n = 1