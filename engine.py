import chess
from concurrent.futures import ThreadPoolExecutor
import logging

logger = logging.getLogger(__name__)
#Search
piece_values = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}

MATE_SCORE = 90000

#Piece-Square Tables
evalWhitePawn = [0,  0,  0,  0,  0,  0,  0,  0,
                50, 50, 50, 50, 50, 50, 50, 50,
                10, 10, 20, 30, 30, 20, 10, 10,
                5,  5, 10, 25, 25, 10,  5,  5,
                0,  0,  0, 20, 20,  0,  0,  0,
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


# Evaluation functions
def evaluate_pieces(board: chess.Board) -> float:
    score = 0
    # adding a score for each piece on a specific square
    for piece_type in piece_values:
        if piece_type == chess.KING:
            continue
        for square in board.pieces(piece_type, chess.WHITE):
            score += PST_White[piece_type][square]

        for square in board.pieces(piece_type, chess.BLACK):
            score -= PST_Black[piece_type][square]

    king_square_white = board.king(chess.WHITE)
    king_square_black = board.king(chess.BLACK)

    if is_endgame(board):
        score += evalWhiteKingEnd[king_square_white]
        score -= evalBlackKingEnd[king_square_black]
    else:
        score += evalWhiteKing[king_square_white]
        score -= evalBlackKing[king_square_black]

    return score


def evaluate(board: chess.Board) -> float:
    """Return a score for the position. Positive -> good for white"""
    score = 0
    positional_score = evaluate_pieces(board)

# Calculating the value of all pieces
    for piece_type in piece_values:
        score += len(board.pieces(piece_type, chess.WHITE)) * piece_values[piece_type]
        score -= len(board.pieces(piece_type, chess.BLACK)) * piece_values[piece_type]

    total = score + positional_score
    logging.DEBUG(
        f"Evaluated score, piece values:{score}, positional values:{positional_score}, total: {total}")
    return total


def is_endgame(board: chess.Board) -> bool:
    queens = 0
    value = 0

    major_pieces = [chess.KNIGHT, chess.BISHOP, chess.ROOK]
    for color in [chess.WHITE, chess.BLACK]:
        queens += len(board.pieces(chess.QUEEN, color))

        for piece in major_pieces:
            value += len(board.pieces(piece, color)) * piece_values[piece]

    if queens == 0 and value < 1300:
        return True

    else:
        return False


# Searching for the best move
def best_move(board: chess.Board, depth: int) -> chess.Move:
    """choosing the best move out of all legal moves using eval func. and minmax"""
    best_move = None
    alpha = float("-inf")
    beta = float("inf")
    logger.info(f"Starting search for depth {depth}. Current FEN: {board.FEN()}")
    if not board.legal_moves:
        logger.debug("No legal moves available")
        return None

    if board.turn == chess.WHITE:
        best_score = float("-inf")
        for legal_move in board.legal_moves:
            board.push(legal_move)
            score = minmax(board, depth-1, alpha, beta)
            alpha = max(alpha, score)
            board.pop()

            if best_score < score:
                best_score = score
                best_move = legal_move
                logger.debug(f"New best score found: {best_score} for move {move.uci()} at depth {depth-1}")
    else:
        best_score = float("inf")
        for legal_move in board.legal_moves:
            board.push(legal_move)
            score = minmax(board, depth-1, alpha, beta)
            beta = min(beta, score)
            board.pop()

            if best_score > score:
                best_score = score
                best_move = legal_move
                logger.debug(f"New best score found: {best_score} for move {move.uci()} at depth {depth-1}")

    return best_move


def minmax(board: chess.Board, depth: int, alpha: float, beta: float) -> float:
    """getting the best score eval func. and minmax,
    by looking at the best move of the opponent and choosing the lesser evil"""
    if depth == 0:
        logger.debug(f"Reached node 0. Score: {evaluate(Board)}")
        return evaluate(board) 

    if board.is_checkmate():
        if board.turn == chess.WHITE:
            logger.debug("White is in CHECKMATE")
            return -MATE_SCORE
        else:
            logger.debug("Black is in CHECKMATE")
            return MATE_SCORE
    if board.is_stalemate() or board.is_insufficient_material() or board.can_claim_threefold_repetition():
        logger.debug("Stalemate has been reached")
        return 0

    if board.turn == chess.WHITE:
        best_score = float("-inf")

        for white_move in board.legal_moves:
            board.push(white_move)
            score = minmax(board, depth-1, alpha, beta)
            best_score = max(best_score, score)
            alpha = max(alpha, score)
            board.pop()

            if alpha >= beta:
                break
    else:
        best_score = float("inf")

        for black_move in board.legal_moves:
            board.push(black_move)
            score = minmax(board, depth-1, alpha, beta)
            best_score = min(best_score, score)
            beta = min(beta, score)
            board.pop()

            if alpha >= beta:
                break

    return best_score
