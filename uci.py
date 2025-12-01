import sys
import chess
from engine import best_move

sys.stdout.reconfigure(line_buffering=True)


def uci_loop():
    board = chess.Board()

    while True:
        line = sys.stdin.readline().strip()

        if line == "":
            continue

        if line == "uci":
            print("id name Schmock3000", flush=True)
            print("id author excylni", flush=True)
            print("uciok", flush=True)

        elif line == "isready":
            print("readyok", flush=True)

        elif line.startswith("position"):
            parts = line.split(" ")

            if "startpos" in parts:
                board = chess.Board()

                if "moves" in parts:
                    idx = parts.index("moves")
                    for mv in parts[idx+1:]:
                        board.push_uci(mv)

            elif "fen" in parts:
                idx = parts.index("fen")
                fen = " ".join(parts[idx+1:idx+7])  # 6 FEN fields
                board = chess.Board(fen)

                if "moves" in parts:
                    idx = parts.index("moves")
                    for mv in parts[idx+1:]:
                        board.push_uci(mv)

        elif line.startswith("go"):
            depth = 4
            move = best_move(board, depth)
            if move is None:
                break
            else:
                print(f"bestmove {move.uci()}", flush=True)

        elif line == "quit":
            break