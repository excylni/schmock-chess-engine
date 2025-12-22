import sys
import chess
import logging
from engine import best_move

sys.stdout.reconfigure(line_buffering=True)
sys.setrecursionlimit(5000)


LOGFILE = "engine_log.txt"

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
    handlers=[
        logging.FileHandler(LOGFILE, mode='a'),
        logging.StreamHandler(sys.stderr)
    ]
)

logging.getLogger().handlers[1].setLevel(logging.WARNING)

move_overhead_ms = 100
threads = 8 


def uci_loop():
    board = chess.Board()

    while True:
        line = sys.stdin.readline().strip()
        logging.debug(f"Received: {line}")

        if line == "":
            continue

        if line == "uci":
            print("id name Schmock3000", flush=True)
            print("id author excylni", flush=True)
            print(f"option name Threads type spin default {threads} min 1 max 8", flush=True)
            print("option name Move Overhead type spin default 100 min 0 max 500", flush=True)
            print("uciok", flush=True)

        elif line == "isready":
            print("readyok", flush=True)

        elif line.startswith("setoption"):
            if "Threads" in line:
                try:
                    threads = int(line.split()[-1])
                    print(f"info string Set Threads = {threads}", flush=True)
                except ValueError:
                    pass
            if "Move Overhead" in line:
                try:
                    move_overhead_ms = int(line.split()[-1])
                    logging.debug(f"Set Move Overhead = {move_overhead_ms} ms")
                except ValueError:
                    pass

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
            print("--- DEBUG: Starting Search Now ---", file=sys.stderr, flush=True)
            wtime = btime = None
            winc = binc = 0
            movestogo = None
            movetime = None

            #Parser
            parts = line.split()
            i = 1
            while i < len(parts):
                token = parts[i]

                if token == "wtime":
                    wtime = int(parts[i+1])
                    i += 2
                elif token == "btime":
                    btime = int(parts[i+1])
                    i += 2
                elif token == "winc":
                    winc = int(parts[i+1])
                    i += 2
                elif token == "binc":
                    binc = int(parts[i+1])
                    i += 2
                elif token == "movestogo":
                    movestogo = int(parts[i+1])
                    i += 2
                elif token == "movetime":
                    movetime = int(parts[i+1])
                    i += 2
                elif token == "infinite":
                    movetime = None
                    i += 1
                else:
                    i += 1

            if board.turn == chess.WHITE:
                time_left = wtime
                inc = winc
            else:
                time_left = btime
                inc = binc

            if movetime is not None:
                think_time = movetime
            elif time_left is not None:
                if movestogo:
                    think_time = time_left // movestogo
                else:
                    think_time = time_left // 30
                think_time += inc
            else:
                think_time = 1000

            think_time = max(10, think_time - move_overhead_ms)
            if think_time < 200:
                depth = 2
            elif think_time < 1000:
                depth = 3
            else:
                depth = 4
            logging.debug(f"Think time allocated: {think_time} ms with depth:{depth}")

            try:
                move = best_move(board, depth)
                if move is None:
                    move = list(board.legal_moves)[0]
                elif move not in board.legal_moves:
                    logging.warning(f"Move {move} is illegal. Choosing first legal move.")
                    move = list(board.legal_moves)[0]
            except Exception as e:
                logging.exception(f"ERROR while calculating best_move {e} for FEN: {board.fen()}")
                move = list(board.legal_moves)[0]

            print(f"bestmove {move.uci()}", flush=True)

        elif line == "quit":
            logging.shutdown()
            break