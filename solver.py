BOARD = [
    [0, 0, 0, 2],
    [3, 0, 0, 0],
    [0, 0, 0, 1],
    [4, 0, 0, 0]
]

class Cell:
    def __init__(self, x, y, value, known=False):
        self.x = x
        self.y = y
        self.value = value
        
        if x < 2:
            if y < 2:
                self.box = 0
            else:
                self.box = 1
        else:
            if y < 2:
                self.box = 2
            else:
                self.box = 3
        
        self.known = known

    def __str__(self):
        return f"x: {self.x}, y: {self.y}, box: {self.box}, value: {self.value}, known: {self.known}"
    
    def knownValue(self):
        return self.value[0]


def initializeCells():
    cells = []

    for x in range(len(BOARD)):
        cells.append([])
        for y in range(len(BOARD[x])):
            if BOARD[x][y] > 0:
                value = [BOARD[x][y]]
                known = True
            else:
                value = [1, 2, 3, 4]
                known = False
            cells[x].append(Cell(x, y, value, known))
            print(cells[x][-1])

    return cells


def inferKnowledge(cells):

    def checkValue(testCell):
        pass

    for row in range(len(cells)):
        for currentCell in cells[row]:
           
            # if value is already known, move to next cell
            if not currentCell.known:
                
                # check row for known values
                for testCell in cells[row]:
                    print(testCell.value, testCell.known)

                    # check if known cell is in current cells list
                    if testCell.known:
                        print('x: ', currentCell.x, currentCell.y)
                        print('known value: ', testCell.value)
                        if testCell.knownValue() in currentCell.value:
                            currentCell.value.remove(testCell.knownValue())
                            print('current cell: ', currentCell.value)
                            print()

                            # # check if only one value remains in the cell and mark as known
                            # if len(currentCell.value) == 1:
                            #     currentCell.known = True
                
                # check columns for known values
                for i in range(4):
                    testCell = cells[i][currentCell.y]
                
                    # check if known cell is in current cells list
                    if testCell.known:
                        if testCell.knownValue() in currentCell.value:
                            currentCell.value.remove(testCell.knownValue())

                            # # check if only one value remains in the cell and mark as known
                            # if len(currentCell.value) == 1:
                            #     currentCell.known = True

                # check box for known values
                if currentCell.box == 0:
                    x, y = 0, 0
                elif currentCell.box == 1:
                    x, y = 2, 0
                elif currentCell.box == 2:
                    x, y = 0, 2
                else:
                    x, y = 2, 2
                
                for i in range(x, x + 2):
                    for j in range(y, y + 2):
                        testCell = cells[i][j]
                        
                        # check if known cell is in current cells list
                        if testCell.known:
                            if testCell.knownValue() in currentCell.value:
                                currentCell.value.remove(testCell.knownValue())

                # check if only one value remains in the cell and mark as known
                if len(currentCell.value) == 1:
                    currentCell.known = True


cells = initializeCells()
print()

inferKnowledge(cells)
print()

inferKnowledge(cells)
print()

inferKnowledge(cells)




print()

for x in range(len(BOARD)):
    for y in range(len(BOARD[x])):
        print(cells[x][y])