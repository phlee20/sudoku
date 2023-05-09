# Code adapted from Kylie Ying


def findNextEmpty(puzzle):
    # Returns the row and col (as Tuple) of an empty cell. If no empty cells, returns None, None
    for row in range(9):
        for col in range(9):
            if puzzle[row][col] == 0:
                return row, col

    return None, None


def isValid(puzzle, guess, row, col):
    # Check if the guess exists in the row and column
    for i in range(9):
        if puzzle[row][i] == guess or puzzle[i][col] == guess:
            return False
    
    # Get the offset values to check if the guess exists in the box
    rowOffset = (row // 3) * 3
    colOffset = (col // 3) * 3

    for i in range(rowOffset, rowOffset + 3):
        for j in range(colOffset, colOffset + 3):
            if puzzle[i][j] == guess:
                return False
    
    return True


def solveSudoku(puzzle):

    # Look for the next empty cell
    row, col = findNextEmpty(puzzle)

    # Base case: If there are no more empty cells, the board is solved since the solver only allows valid entries
    if row == None:
        return True
    
    # Try every possible value for the cell.
    # If it's valid, set the value and recursively call the solver for the next empty cell.
    for guess in range(1, 10):

        if isValid(puzzle, guess, row, col):
            puzzle[row][col] = guess
            if solveSudoku(puzzle):
                return True

        # If the guess is not valid or there are no future guesses that are valid, then backtrack to try a new guess
        # Reset the cell
        puzzle[row][col] = 0
    
    return False


