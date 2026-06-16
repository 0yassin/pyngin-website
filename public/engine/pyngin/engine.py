from pyngin.moves import get_legal_moves, get_move_score
from pyngin.evaluate import get_relative_eval

def get_engine_move(board, d, game_history=None):
    if game_history == None:
        game_history = []
    best_move = None
    best_score = -float('inf')
    alpha, beta = -float('inf'), float('inf')
    legal_moves = get_legal_moves(board)
    if not legal_moves:
        return None

    legal_moves.sort(key=lambda m:get_move_score(m, board), reverse=True)
    
    for move in legal_moves:
        temp_board = board.clone()
        temp_board.make_move(move)

        score = -negamax(temp_board, d - 1, -beta, -alpha, ply=1, history=game_history)

        if score > best_score:
            best_score = score
            best_move = move
        alpha = max(alpha, score)
    return best_move

def negamax(board, d, alpha, beta,ply=0, history=None):
    if history is None:
        history = []

    current_position_id = (tuple(board.state), board.turn)
    if current_position_id in history:
        return 0 

    if d == 0:
        if board.is_in_check():
            if not get_legal_moves(board):
                return -100000000 + ply
        return get_relative_eval(board)

    legal_moves = get_legal_moves(board)
    
    if len(legal_moves) == 0:
        if board.is_in_check():
            return -100000000 + ply
        else:
            return 0  

    legal_moves.sort(key=lambda m:get_move_score(m, board), reverse=True)
    max_eval = -float('inf')
    history.append(current_position_id)
    for move in legal_moves:
        temp_board = board.clone()
        temp_board.make_move(move)
        evaluation = -negamax(temp_board, d - 1, -beta, -alpha, ply + 1, history=history)
        max_eval = max(max_eval, evaluation)
        alpha = max(alpha, evaluation)
        if alpha >= beta:
            break

    history.pop()
    return max_eval