from pyngin.converter import load_fen
from pyngin.board import Board
from logging import error
from pyngin.moves import get_legal_moves
import time

def perft(d, board):
    if d == 0: return 1
    lmoves = get_legal_moves(board)
    nodes = 0
    for lmove in lmoves:
        state_inf = board.make_move(lmove)
        nodes += perft(d - 1, board)
        board.unmake_move(lmove, state_inf)
    return nodes

def perft_benchmark(board=None):
    if board is None:
        board = Board()
    load_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", board)
    print("==========================================")
    start_time = time.time()
    p = perft(1, board)
    elapsed = time.time() - start_time
    nps = int(p / elapsed) if elapsed > 0 else 0
    if p == 20:
        print(f"PERFT at depth 1: SUCCESS (20) in {elapsed:.2f}s ({nps} nodes/s)")
    else:
        error(f"PERFT at depth 1: FAILED {p}")
    start_time = time.time()
    p = perft(2, board)
    elapsed = time.time() - start_time
    nps = int(p / elapsed) if elapsed > 0 else 0
    if p == 400:
        print(f"PERFT at depth 2: SUCCESS (400) in {elapsed:.2f}s ({nps} nodes/s)")
    else:
        error(f"PERFT at depth 2: FAILED {p}")

    start_time = time.time()
    p = perft(3, board)
    elapsed = time.time() - start_time
    nps = int(p / elapsed) if elapsed > 0 else 0
    if p == 8902:
        print(f"PERFT at depth 3: SUCCESS (8902) in {elapsed:.2f}s ({nps} nodes/s)")
    else:
        error(f"PERFT at depth 3: FAILED {p}")

    start_time = time.time()
    p = perft(5, board)
    elapsed = time.time() - start_time
    nps = int(p / elapsed) if elapsed > 0 else 0
    if p == 197281:
        print(f"PERFT at depth 4 SUCESS (197,281) in {elapsed:.2f}s ({nps} nodes/s)")
    else:
        error(f"PERFT depth 4: FAILED {p}")
    print("===========================================")
    return
