import chess
from concurrent.futures import ThreadPoolExecutor
import logging
import time

logger = logging.getLogger(__name__)


class SearchTimeout(Exception):
    pass

#Piece-Square Tables
evalWhitePawn = [0,  0,  0,  0,  0,  0,  0,  0,
                50, 50, 50, 50, 50, 50, 50, 50,
                10, 10, 20, 30, 30, 20, 10, 10,
                5,  5, 10, 25, 25, 10,  5,  5,
                0,  0,  0, 30, 30,  0,  0,  0,
                5, -5,-10,  0,  0,-10, -5,  5,
                5, 10, 10,-20,-20, 10, 10,  5,
                0,  0,  0,  0,  0,  0,  0,  0]

evalBlackPawn = list(reversed(evalWhitePawn))

evalWhiteKnight = [-50,-40,-30,-30,-30,-30,-40,-50,
                  -40,-20,  0,  0,  0,  0,-20,-40,
                  -30,  0, 10, 15, 15, 10,  0,-30,
                  -30,  5, 15, 20, 20, 15,  5,-30,
                  -30,  0, 15, 20, 20, 15,  0,-30,
                  -30,  5, 10, 15, 15, 10,  5,-30,
                  -40,-20,  0,  5,  5,  0,-20,-40,
                  -50,-40,-30,-30,-30,-30,-40,-50,]

evalBlackKnight = list(reversed(evalWhiteKnight))

evalWhiteBishop = [-20,-10,-10,-10,-10,-10,-10,-20,
                  -10,  0,  0,  0,  0,  0,  0,-10,
                  -10,  0,  5, 10, 10,  5,  0,-10,
                  -10,  5,  5, 10, 10,  5,  5,-10,
                  -10,  0, 10, 10, 10, 10,  0,-10,
                  -10, 10, 10, 10, 10, 10, 10,-10,
                  -10,  5,  0,  0,  0,  0,  5,-10,
                  -20,-10,-10,-10,-10,-10,-10,-20,]

evalBlackBishop = list(reversed(evalWhiteBishop))

evalWhiteRook = [  0,  0,  0,  0,  0,  0,  0,  0,
                  5, 10, 10, 10, 10, 10, 10,  5,
                 -5,  0,  0,  0,  0,  0,  0, -5,
                 -5,  0,  0,  0,  0,  0,  0, -5,
                 -5,  0,  0,  0,  0,  0,  0, -5,
                 -5,  0,  0,  0,  0,  0,  0, -5,
                 -5,  0,  0,  0,  0,  0,  0, -5,
                  0,  0,  0,  5,  5,  0,  0,  0]

evalBlackRook  = list(reversed(evalWhiteRook))

evalWhiteQueen = [-20,-10,-10, -5, -5,-10,-10,-20,
                 -10,  0,  0,  0,  0,  0,  0,-10,
                 -10,  0,  5,  5,  5,  5,  0,-10,
                 -5,  0,  5,  5,  5,  5,  0, -5,
                  0,  0,  5,  5,  5,  5,  0, -5,
                 -10,  5,  5,  5,  5,  5,  0,-10,
                 -10,  0,  5,  0,  0,  0,  0,-10,
                 -20,-10,-10, -5, -5,-10,-10,-20]

evalBlackQueen = list(reversed(evalWhiteQueen))

evalWhiteKing = [-30,-40,-40,-50,-50,-40,-40,-30,
                 -30,-40,-40,-50,-50,-40,-40,-30,
                 -30,-40,-40,-50,-50,-40,-40,-30,
                 -30,-40,-40,-50,-50,-40,-40,-30,
                 -20,-30,-30,-40,-40,-30,-30,-20,
                 -10,-20,-20,-20,-20,-20,-20,-10,
                  20, 20,  0,  0,  0,  0, 20, 20,
                  20, 30, 10,  0,  0, 10, 30, 20]

evalBlackKing = list(reversed(evalWhiteKing))

#Endgame
evalWhiteKingEnd = [-50,-40,-30,-20,-20,-30,-40,-50,
                    -30,-20,-10,  0,  0,-10,-20,-30,
                    -30,-10, 20, 30, 30, 20,-10,-30,
                    -30,-10, 30, 40, 40, 30,-10,-30,
                    -30,-10, 30, 40, 40, 30,-10,-30,
                    -30,-10, 20, 30, 30, 20,-10,-30,
                    -30,-30,  0,  0,  0,  0,-30,-30,
                    -50,-30,-30,-30,-30,-30,-30,-50]

evalBlackKingEnd = list(reversed(evalWhiteKingEnd))

PST_White = {
    chess.PAWN: evalWhitePawn,
    chess.KNIGHT: evalWhiteKnight,
    chess.BISHOP: evalWhiteBishop,
    chess.ROOK: evalWhiteRook,
    chess.QUEEN: evalWhiteQueen,
}

PST_Black = {
    chess.PAWN: evalBlackPawn,
    chess.KNIGHT: evalBlackKnight,
    chess.BISHOP: evalBlackBishop,
    chess.ROOK: evalBlackRook,
    chess.QUEEN: evalBlackQueen,
}


class ChessEngine():
    def __init__(self, board: chess.Board = None):
        self.name = "Schmock3000"
        self.board = board if board else chess.Board()
        self.piece_values = {
            chess.PAWN: 100,
            chess.KNIGHT: 320,
            chess.BISHOP: 330,
            chess.ROOK: 500,
            chess.QUEEN: 900,
            chess.KING: 20000
            }
        self.MATE_SCORE = 90000
        self.nodes_visited = 0

    def evaluate_pieces(self, board: chess.Board) -> float:
        score = 0
        # adding a score for each piece on a specific square
        for piece_type in self.piece_values:
            if piece_type == chess.KING:
                continue
            for square in board.pieces(piece_type, chess.WHITE):
                score += PST_White[piece_type][square]

            for square in board.pieces(piece_type, chess.BLACK):
                score -= PST_Black[piece_type][square]

        king_square_white = board.king(chess.WHITE)
        king_square_black = board.king(chess.BLACK)

        if self.is_endgame(board):
            score += evalWhiteKingEnd[king_square_white]
            score -= evalBlackKingEnd[king_square_black]
        else:
            score += evalWhiteKing[king_square_white]
            score -= evalBlackKing[king_square_black]

        return score

    def evaluate(self, board: chess.Board) -> float:
        """Return a score for the position. Positive -> good for white"""
        score = 0
        positional_score = self.evaluate_pieces(self.board)

    # Calculating the value of all pieces
        for piece_type in self.piece_values:
            score += len(board.pieces(piece_type, chess.WHITE)) * self.piece_values[piece_type]
            score -= len(board.pieces(piece_type, chess.BLACK)) * self.piece_values[piece_type]

        total = score + positional_score
        logging.debug(
            f"Evaluated score, piece values:{score}, positional values:{positional_score}, total: {total}")
        return total

    def is_endgame(self, board: chess.Board) -> bool:
        queens = 0
        value = 0

        major_pieces = [chess.KNIGHT, chess.BISHOP, chess.ROOK]
        for color in [chess.WHITE, chess.BLACK]:
            queens += len(board.pieces(chess.QUEEN, color))

            for piece in major_pieces:
                value += len(board.pieces(piece, color)) * self.piece_values[piece]

        if queens == 0 and value < 1300:
            return True

        else:
            return False

    def minimax(self, board: chess.Board, depth: int, alpha: float, beta: float, start_time: float, think_time: float) -> float:
        """getting the best score eval func. and minimax,
        by looking at the best move of the opponent and choosing the lesser evil"""
        best_move = None
        self.nodes_visited += 1

        if self.nodes_visited % 2048 == 0:
            elapsed = time.time() - start_time

            if elapsed > think_time:
                raise SearchTimeout

        if board.is_game_over():
            result = board.outcome()
            if result.winner is None:
                return 0.0, None  # Draw (Stalemate, repetition, etc.)
            return (self.MATE_SCORE, None) if result.winner == chess.WHITE else (-self.MATE_SCORE, None)

        if depth == 0:
            return self.evaluate(board), None

        if board.turn == chess.WHITE:
            best_score = float("-inf")

            for white_move in board.legal_moves:
                board.push(white_move)
                score, _ = self.minimax(board, depth-1, alpha, beta, think_time, start_time)
                if best_score < score:
                    best_score = score
                    best_move = white_move
                alpha = max(alpha, best_score)
                board.pop()

                if alpha >= beta:
                    break
        else:
            best_score = float("inf")

            for black_move in board.legal_moves:
                board.push(black_move)
                score, _ = self.minimax(board, depth-1, alpha, beta, think_time, start_time)
                if best_score > score:
                    best_score = score
                    best_move = black_move
                beta = min(beta, best_score)
                board.pop()

                if alpha >= beta:
                    break

        return best_score, best_move

    def itterative_deepening(self, board: chess.Board, time_left: float):
        """starting search from depth 0 and increasing """
        best_move = None
        start_time = time.time()

        limit = time_left // 1000
        think_time = limit / 18
        self.nodes_visited = 0
        for depth in range(0, 1000):
            elapsed = time.time() - start_time

            # if no time left, break
            if elapsed > think_time:
                break

            try:
                _, move = self.minimax(
                    board,
                    depth,
                    float("inf"),
                    float("-inf"),
                    start_time,
                    think_time)
                if move:
                    best_move = move

            except SearchTimeout:
                print(f"Ran out of time! Stopped at depth {depth}. Nodes reached: {self.nodes_visited}") 

        return best_move