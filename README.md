# sudoku

Two implementations of a sudoku solver.

The inference method stores knowledge about known cells and possible values for unknown cells to deduce the solution in a two-step process.
Step 1 is checking the known cells and eliminating them as possibilities for each unknown cell.
Step 2 is checking the possible values in unknown cells in deducing if there exists a possible value that is unique to a row, column or box. If there is, make that cell known and remove other possible values from that cell.
Repeat until a solution is found or no new knowledge can be deduced.
I tested it with a few expert level 3x3 sudoku's and they were all solved. It's possible a solution may not be found. More advanced deduction techniques would need to be written.

The backtrack method uses trial and error to makes guesses for each cell and recurse through the problem. If a contradiction is found, the algorithm backtracks to try a different value. As long as the sudoku is solvable, it will be solved.
This solution was adapted from Kylie Ying's implementation.

Runtime for both methods is calculated and printed in the terminal. Seems that inference is about 100x faster but given the small size of the problem, the difference is negligable as both come in under 1 second.

Could potentially extend this for a 4x4 or even a 5x5 board using hexademical or alphanumeric to see if it makes a difference.
