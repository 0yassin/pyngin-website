from pyngin.moves import translate_move
from pyngin.converter import load_fen
from pyngin.board import Board
from pyngin.engine import get_engine_move


def get_best_move(fen:str, depth:int):
    board = Board()
    load_fen(fen, board)
    engine_move = get_engine_move(board, depth)
    return translate_move(engine_move)