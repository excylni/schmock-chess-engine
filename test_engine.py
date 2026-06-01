import pytest 
import chess
import time
from engine import ChessEngine

@pytest.fixture
def bot():
    """Create a fresh engine for testing"""
    return ChessEngine()


def test_legal_move(bot):
    """test to see if our engine gives us a legal move"""
    board = chess.Board()
    chosen_move = bot.itterative_deepening(board, 10)

    assert chosen_move is not None
    assert chosen_move in board.legal_moves


def test_hanging_queen(bot):
    """Verify if engine takes queen"""
    board = chess.Board("r1bk3r/p2pBpNp/n4n2/1p1NP2P/6P1/3P4/P1P1K3/q5b1 b - - 0 1")

    chosen_move = bot.itterative_deepening(board, 2)
    assert chosen_move is None


def test_evaluate_pieces(bot):
    board = chess.Board()
    evaluation = bot.evaluate_pieces(board)
    assert isinstance(evaluation, (int, float))

def test_performance(bot):
    fen = ("7B/3B1p2/rP1p2R1/n2k1Pb1/N2Pp3/4P3/K2nN1r1/2R5")
    board = chess.Board(fen)
    time_left = 10000

    # Start our test
    start_real_time = time.time()
    chosen_move = bot.itterative_deepening(board, time_left)
    elapsed_time =time.time() - start_real_time 


    total_nodes = bot.nodes_visited
    nps = total_nodes / elapsed_time if elapsed_time > 0 else 0

    print(f"Position:       {fen}")
    print(f"Time Taken:      {elapsed_time:.3f} seconds")
    print(f"Nodes Visited:   {total_nodes:,} nodes")
    print(f"Calculated Speed: {int(nps):,} NPS (Nodes Per Second)")
    print(f"Selected Move:   {chosen_move}")

    assert chosen_move is not None, "Engine failed to select a move"
    assert total_nodes > 0, "Performance Failure: The engine visited 0 nodes!"