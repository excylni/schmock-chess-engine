Created a chess engine with the help of python-chess library. engine.py contains our evaluation and search function. UCI is our protocoll for communicating with chess GUIs.


## ver 1.1
- added itterative deepening for better pruning and time management

Performance test:

Ran out of time! Stopped at depth 4. Nodes reached: 6144
Position:       7B/3B1p2/rP1p2R1/n2k1Pb1/N2Pp3/4P3/K2nN1r1/2R5
Time Taken:      0.677 seconds
Nodes Visited:   6,144 nodes
Calculated Speed: 9,075 NPS (Nodes Per Second)
Selected Move:   h8e5


## ver 1.0

- implemented search function with minimax algorithm and alpha-beta pruning
- evaluation is simply just calculating piece values with Piece-Square-Tables


