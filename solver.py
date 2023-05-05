BOARD = [
    [0, 0, 0, 2],
    [3, 0, 0, 0],
    [0, 0, 0, 1],
    [4, 0, 0, 0]
]

class Cell:
    def __init__(self, row, col, value, known=False):
        self.row = row
        self.col = col
        self.value = value
        
        if row < 2:
            if col < 2:
                self.box = 0
            else:
                self.box = 1
        else:
            if col < 2:
                self.box = 2
            else:
                self.box = 3
        
        self.known = known


    def __eq__(self, other):
        return self.row == other.row and self.col == other.col


    def __str__(self):
        return f"row: {self.row}, col: {self.col}, box: {self.box}, value: {self.value}, known: {self.known}"
    

    def knownValue(self):
        return self.value[0]


    def remove(self, value):
        self.value.remove(value)


def initializeCells():
    cells = []

    for row in range(len(BOARD)):
        cells.append([])
        for col in range(len(BOARD[row])):
            if BOARD[row][col] > 0:
                value = [BOARD[row][col]]
                known = True
            else:
                value = [1, 2, 3, 4]
                known = False
            cells[row].append(Cell(row, col, value, known))
            print(cells[row][-1])

    return cells


def inferKnowledge(cells):

    def compareValues(testCell):
        # check if known cell is in current cells list
        if testCell != currentCell and testCell.known:

            if testCell.knownValue() in currentCell.value:
                currentCell.remove(testCell.knownValue())

                # check if only one value remains in the cell and mark as known
                if len(currentCell.value) == 1:
                    currentCell.known = True
                    return 'Found'


    def checkSeriesIceCream():
        # check row for known values
        for testCell in cells[i]:
            if compareValues(testCell) == 'Found':
                return
        
        # check columns for known values
        for j in range(4):
            testCell = cells[j][currentCell.col]
            if compareValues(testCell) == 'Found':
                return

        # check box for known values
        if currentCell.box == 0:
            x, y = 0, 0
        elif currentCell.box == 1:
            x, y = 2, 0
        elif currentCell.box == 2:
            x, y = 0, 2
        else:
            x, y = 2, 2
        
        for k in range(x, x + 2):
            for m in range(y, y + 2):
                testCell = cells[m][k]
                if compareValues(testCell) == 'Found':
                    return
             

    for i in range(len(cells)):
        for currentCell in cells[i]:
           
            # if value is already known, move to next cell
            if not currentCell.known:
                checkSeriesIceCream()
                

cells = initializeCells()
print()

inferKnowledge(cells)
print()

inferKnowledge(cells)
print()

# inferKnowledge(cells)




print()

for x in range(len(BOARD)):
    for y in range(len(BOARD[x])):
        print(cells[x][y])