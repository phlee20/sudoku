from math import sqrt
import simple_colors as sc


class Cell:
    def __init__(self, row, col, box, value, default, known=False):
        self.row = row
        self.col = col
        self.value = value
        self.box = box
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
    

class Knowledge:
    def __init__(self, size):
        self.rows = {i:set() for i in range(size)}
        self.columns = {i:set() for i in range(size)}
        self.boxes = {i:set() for i in range(size)}


    def populate(self, row, col, box, value):
        self.rows[row].update(value)
        self.columns[col].update(value)
        self.boxes[box].update(value)

    def update(self, currentCell, value):
        self.rows[currentCell.row].add(value)
        self.columns[currentCell.col].add(value)
        self.boxes[currentCell.box].add(value)


class Board:
    
    def __init__(self, board):
        self.cells = []
        self.board = board
        self.size = len(self.board)

        self.knowledge = Knowledge(self.size)

    
    def initializeCells(self):
        boxSize = int(sqrt(self.size))
        add = self.size > 9 and 0 or 1

        for row in range(self.size):
            self.cells.append([])
            for col in range(self.size):
                box = row // boxSize * boxSize + col // boxSize
                if self.board[row][col] != -1:
                    value = [self.board[row][col]]
                    default = True
                    known = True

                    self.knowledge.populate(row, col, box, value)
                else:
                    # Generate default values for empty squares
                    value = [num + add for num in range(self.size)]
                    default = False
                    known = False

                self.cells[row].append(Cell(row, col, box, value, default, known))
        
                # DEBUG: print(self.cells[row][-1])
    
    def printBoard(self):
        for row in self.cells:
            for cell in row:
                if cell.box == 1:
                    print(cell)

    
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


    def checkSeries(self, currentCell, i):

        rowSet = self.knowledge.rows[currentCell.row]
        colSet = self.knowledge.columns[currentCell.col]
        boxSet = self.knowledge.boxes[currentCell.box]

        flag = False

        for value in reversed(currentCell.value):
            knownValues = rowSet.union(colSet.union(boxSet))

            if value in knownValues:
                currentCell.remove(value)
                flag = True

                
        if len(currentCell.value) == 1:
            currentCell.known = True

            rowSet.update(currentCell.value)
            colSet.update(currentCell.value)
            boxSet.update(currentCell.value)
                
            flag = True

        # check box for unknown values
        for value in currentCell.value:
            if self.checkUnknownBox(value, currentCell) == 'Found':
               flag = True
            if self.checkUnknownRow(value, currentCell) == 'Found':
               flag = True
            if self.checkUnknownColumn(value, currentCell) == 'Found':
               flag = True

        return flag


    def checkUnknownRow(self, value, currentCell):

        # loop through row items to see if a value only exists in current cell
        for testCell in self.cells[currentCell.row]:
            if testCell != currentCell and not testCell.known:
                if value in testCell.value:
                    return
        
        # if value does not exists in other cells' potential list, make it the known value by removing other values
        for num in reversed(currentCell.value):
            if num != value:
                currentCell.remove(num)
                currentCell.known = True

        self.knowledge.update(currentCell, value)

        return 'Found'
    

    def checkUnknownColumn(self, value, currentCell):
        # loop through row items to see if a value only exists in current cell
        for j in range(self.size):
            testCell = self.cells[j][currentCell.col]
            if testCell != currentCell and not testCell.known:
                if value in testCell.value:
                    return
        
        # if value does not exists in other cells' potential list, make it the known value by removing other values
        for num in reversed(currentCell.value):
            if num != value:
                currentCell.remove(num)
                currentCell.known = True

        self.knowledge.update(currentCell, value)

        return 'Found'


    def checkUnknownBox(self, value, currentCell):
        increase = int(sqrt(self.size))
        rowStart = (currentCell.row // increase) * increase
        colStart = (currentCell.col // increase) * increase
        
        # loop through box items to see if a value only exists in current cell
        for row in range(rowStart, rowStart + increase):
            for col in range(colStart, colStart + increase):
                testCell = self.cells[row][col]
                if testCell != currentCell and not testCell.known:
                    if value in testCell.value:
                        return
        
        # if value does not exists in other cells' potential list, make it the known value by removing other values
        for num in reversed(currentCell.value):
            if num != value:
                currentCell.remove(num)
                currentCell.known = True
        
        self.knowledge.update(currentCell, value)

        return 'Found'
    

    def inferKnowledge(self):
        newChanges = False

        for i in range(self.size):
            for currentCell in self.cells[i]:
            
                # if value is already known, move to next cell
                if not currentCell.known:
                    if self.checkSeries(currentCell, i):
                        newChanges = True

        if newChanges:
            self.inferKnowledge()
