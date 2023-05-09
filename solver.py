"""
    Sudoku Solver Comparison
    by: Philip Lee

    Compares two approaches to solving a sudoku.
    Inference solves a sudoku puzzle without making any wrong guesses. Uses knowledge to infer correct guesses.
    Backtrack solves a sudoku puzzle using recursion and backtracking wrong guesses.

    The runtime for both are shown at the end.
"""

import time
import inference
import backtrack

# 2x2 board
BOARD4 = [
    [0, 0, 0, 3],
    [0, 2, 0, 0],
    [0, 0, 3, 0],
    [4, 0, 0, 0]
]

# 3x3 board
BOARD9= [
    [0, 0, 7, 8, 9, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 5, 0, 0],
    [0, 8, 0, 0, 6, 0, 3, 0, 9],
    [0, 9, 0, 0, 0, 0, 0, 5, 0],
    [0, 0, 4, 0, 0, 3, 9, 0, 1],
    [0, 0, 0, 0, 1, 0, 0, 7, 0],
    [2, 0, 0, 0, 0, 4, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 7, 0, 0, 3, 0, 8, 0, 6]
]

# Run the backtrack solver and measure time to solve
backtrackStart = time.time()    
print(backtrack.solveSudoku(BOARD9))
print(BOARD9)
backtrackEnd = time.time()

# Run the inference solver and measure time to solve
inferenceStart = time.time()    
board = inference.Board(BOARD9)
board.initializeCells()
board.printLayout()
board.inferKnowledge()
board.printLayout()
inferenceEnd = time.time()

print('Backtrack Runtime: ' + str(round(backtrackEnd - backtrackStart, 6)) + 's')
print('Inference Runtime: ' + str(round(inferenceEnd - inferenceStart, 6)) + 's')
