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

def test_best_move_returns_none_on_checkmate(bot):
    """Verify engine returns None if it's already checkmate."""
    # Fool's Mate position (Black has won)
    board = chess.Board("rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 0 3")
    
    move = bot.best_move(board, depth=1)
    assert move is None

def test_evaluate_pieces(bot):
    board = chess.Board()
    evaluation = bot.evaluate_pieces(board)
    assert isinstance(evaluation, (int,float))



