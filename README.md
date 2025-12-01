Created a chess engine with the help of python-chess library. engine.py contains our evaluation and search function. UCI is our protocoll for communicating with chess GUIs.

## ver 1.0

- search function has minimax algorithm with alpha-beta pruning
- evaluation is simply just calculating pieces not captured pieces with their values
- also penalizing repetetive moves 
