from math import sqrt
import simple_colors as sc

BOARD4 = [
    [0, 0, 0, 3],
    [0, 2, 0, 0],
    [0, 0, 3, 0],
    [4, 0, 0, 0]
]


BOARD9 = [
    [2, 0, 0, 5, 1, 0, 0, 0, 4],
    [4, 0, 9, 0, 6, 8, 0, 0, 0],
    [0, 0, 8, 0, 0, 0, 0, 7, 0],
    [0, 0, 0, 8, 9, 0, 7, 2, 0],
    [1, 0, 0, 0, 0, 5, 0, 0, 0],
    [0, 0, 2, 0, 0, 0, 5, 0, 8],
    [0, 6, 1, 0, 0, 0, 0, 9, 0],
    [0, 2, 4, 1, 3, 9, 8, 0, 6],
    [0, 5, 3, 0, 8, 2, 4, 1, 7]
]

BOARD9_2 = [
    [7, 8, 0, 0, 0, 0, 1, 0, 3],
    [0, 0, 0, 0, 3, 0, 2, 7, 0],
    [0, 0, 2, 9, 0, 0, 0, 0, 0],
    [0, 6, 7, 4, 8, 0, 0, 0, 0],
    [2, 9, 0, 3, 0, 0, 0, 4, 0],
    [0, 0, 0, 0, 7, 0, 0, 0, 1],
    [0, 0, 0, 0, 9, 6, 0, 0, 8],
    [9, 5, 8, 0, 4, 3, 7, 6, 0],
    [0, 7, 3, 0, 5, 2, 4, 1, 9]
]


BOX_OFFSET = {
    4: {
        0: (0, 0),
        1: (2, 0),
        2: (0, 2),
        3: (2, 2)
    },
    9: {
        0: (0, 0),
        1: (3, 0),
        2: (6, 0),
        3: (0, 3),
        4: (3, 3),
        5: (6, 3),
        6: (0, 6),
        7: (3, 6),
        8: (6, 6)
    }
}


class Cell:
    def __init__(self, row, col, size, value, default, known=False):
        self.row = row
        self.col = col
        self.value = value
        self.box = self.size(size)
        self.default = default
        self.known = known


    def __eq__(self, other):
        return self.row == other.row and self.col == other.col


    def __str__(self):
        return f"row: {self.row}, col: {self.col}, box: {self.box}, value: {self.value}, known: {self.known}"
    

    def knownValue(self):
        return self.value[0]


    def remove(self, value):
        self.value.remove(value)


    def size(self, size):
        if size == 4:
            if self.row < 2:
                if self.col < 2:
                    box = 0
                else:
                    box = 1
            else:
                if self.col < 2:
                    box = 2
                else:
                    box = 3
        elif size == 9:
            if self.row < 3:
                if self.col < 3:
                    box = 0
                elif self.col < 6:
                    box = 1
                else:
                    box = 2
            elif self.row < 6:
                if self.col < 3:
                    box = 3
                elif self.col < 6:
                    box = 4
                else:
                    box = 5
            else:
                if self.col < 3:
                    box = 6
                elif self.col < 6:
                    box = 7
                else:
                    box = 8

        return box


class Board:
    def __init__(self, board):
        self.cells = []
        self.board = board
        self.size = len(self.board)

    
    def initializeCells(self):
        for row in range(self.size):
            self.cells.append([])
            for col in range(self.size):
                if self.board[row][col] > 0:
                    value = [self.board[row][col]]
                    default = True
                    known = True
                else:
                    # Generate default values for empty squares
                    value = [num + 1 for num in range(self.size)]
                    default = False
                    known = False
                self.cells[row].append(Cell(row, col, self.size, value, default, known))
                print(self.cells[row][-1])

    
    def printBoard(self):
        for x in range(self.size):
            for y in range(self.size):
                print(self.cells[x][y])

    
    def printLayout(self):
        size = sqrt(self.size)
        print("-------------------------")
        for x in range(self.size):
            print("|", end=" ")
            for y in range(self.size):
                if len(self.cells[x][y].value) > 1:
                    print('X', end=" ")
                else:
                    if self.cells[x][y].default:
                        print(sc.blue(self.cells[x][y].value[0]), end=" ")
                    else:
                        print(sc.red(self.cells[x][y].value[0]), end=" ")
                if (y + 1) % size == 0:
                    print("|", end=" ")
            print()
            if (x + 1) % size == 0:
                print("-------------------------")


    def compareValues(self, testCell, currentCell):
        # check if known cell is in current cells list
        if testCell != currentCell and testCell.known:

            if testCell.knownValue() in currentCell.value:
                currentCell.remove(testCell.knownValue())

                # check if only one value remains in the cell and mark as known
                if len(currentCell.value) == 1:
                    currentCell.known = True
                    return 'Found'


    def checkSeries(self, currentCell, i):
        # check row for known values
        for testCell in self.cells[i]:
            if self.compareValues(testCell, currentCell) == 'Found':
                return
        
        # check columns for known values
        for j in range(self.size):
            testCell = self.cells[j][currentCell.col]
            if self.compareValues(testCell, currentCell) == 'Found':
                return

        x, y = BOX_OFFSET[self.size][currentCell.box]
        increase = int(sqrt(self.size))
        
        for k in range(x, x + increase):
            for m in range(y, y + increase):
                testCell = self.cells[m][k]
                if self.compareValues(testCell, currentCell) == 'Found':
                    return


    def inferKnowledge(self):

        for i in range(self.size):
            for currentCell in self.cells[i]:
            
                # if value is already known, move to next cell
                if not currentCell.known:
                    self.checkSeries(currentCell, i)
                



board = Board(BOARD9_2)
board.initializeCells()
print()
board.inferKnowledge()
print()
board.inferKnowledge()
print()
board.inferKnowledge()
print()
board.inferKnowledge()
print()
board.inferKnowledge()
print()

board.printBoard()
board.printLayout()