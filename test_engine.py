import pytest 
import chess
from engine import ChessEngine

@pytest.fixture
def bot():
    """Create a fresh engine for testing"""
    return ChessEngine()


def test_legal_move(bot):
    """test to see if our engine gives us a legal move"""
    board = chess.Board()
    move = bot.best_move(board, 3)

    assert move is not None
    assert move in board.legal_moves


def test_hanging_queen(bot):
    """Verify if engine takes queen"""
    board = chess.Board("r1bk3r/p2pBpNp/n4n2/1p1NP2P/6P1/3P4/P1P1K3/q5b1 b - - 0 1")

    move = bot.best_move(board, depth=1)
    assert move is None


def test_evaluate_pieces(bot):
    board = chess.Board()
    evaluation = bot.evaluate_pieces(board)
    assert isinstance(evaluation, (int, float))

