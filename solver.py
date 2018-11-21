class Square:
    def __init__(self, index):
        self.possibleValues = {1,2,3,4,5,6,7,8,9}
        self.index = index

    def Set(self, value):
        if self.IsSolved() and self.Value != value:
            raise Exception("Changing a solved square's value to another value!")
        self.possibleValues = {value}

    def Remove(self, value):
        self.possibleValues.discard(value)

    def Value(self):
        if not self.IsSolved():
            raise Exception("Cannot get the value if the square isn't solved.")
        # possibleValues is a set and cannot be indexed
        return next(iter(self.possibleValues))
    
    def IsSolved(self):
        return len(self.possibleValues) == 1

# Helpers
#===============

def CreateSudoku():
    return [Square(i) for i in range(81)]

def GetRow(rowIndex, sudoku):
    start = rowIndex * 9
    stop = start + 9
    return sudoku[slice(start, stop)]

def GetTheOtherSquaresInSameRow(squareIndex, sudoku):
    rowIndex = squareIndex // 9
    row = GetRow(rowIndex, sudoku)
    return  filter(lambda x: x.index != squareIndex, row)

def GetTheOtherSquaresInSameCol(squareIndex, sudoku):
    colIndex = squareIndex % 9
    col = sudoku[slice(colIndex, None, 9)]
    return filter(lambda x: x.index != squareIndex, col)

def GetBigSquareIndex(squareIndex):
    rowIndex = squareIndex // (9 * 3)
    colIndex = (squareIndex // 3) % 3
    return rowIndex * 3 + colIndex

def GetIndicesInBigSquare(bigSquareIndex):
    row = bigSquareIndex // 3
    col = bigSquareIndex % 3
    startIndex = row * 27 + col * 3
    return {
        startIndex, startIndex + 1, startIndex + 2,
        startIndex + 9, startIndex + 10, startIndex + 11,
        startIndex + 18, startIndex + 19, startIndex + 20
        }

def GetSquaresInBigSquare(bigSquareIndex, sudoku):
    indices = GetIndicesInBigSquare(bigSquareIndex)
    return [sudoku[i] for i in indices]

def GetTheOtherSquaresInTheBigSquare(squareIndex, sudoku):
    bigSquareIndex = GetBigSquareIndex(squareIndex)
    squares = GetSquaresInBigSquare(bigSquareIndex, sudoku)
    return filter(lambda x: x.index != squareIndex, squares)

# Printing
#======================

def GetSquareString(possibleSquareValues):
    if len(possibleSquareValues) == 9:
        val = "1-9" 
    else: 
        val = "".join([str(i) for i in possibleSquareValues])
    return val.rjust(8)

def GetSudokuBigSquareRowString(bigSquareRow):
    squareStrings = [GetSquareString(square.possibleValues) for square in bigSquareRow]
    return " ".join(squareStrings)

def GetSudokuRowString(row):
    rowParts = [row[i:i+3] for i in range(0, len(row), 3)]
    left = GetSudokuBigSquareRowString(rowParts[0])
    middle = GetSudokuBigSquareRowString(rowParts[1])
    right = GetSudokuBigSquareRowString(rowParts[2])
    return f"| {left} | {middle} | {right} |"

def PrintSudoku(sudoku):
    horizontalDelimiter = "-" * 88

    rows = list()
    rows.append(horizontalDelimiter)
    for rowIndex in range(9):
        row = GetRow(rowIndex, sudoku)
        rowStr = GetSudokuRowString(row)
        rows.append(rowStr)
        if rowIndex > 0 and rowIndex % 3 == 2:
            rows.append(horizontalDelimiter)
    print("\n".join(rows))   

# Logic
#===============

def TranslateFromUserIndices(biqSquareIndex, smallSquareIndex):
    row = (biqSquareIndex // 3) * 3 + smallSquareIndex // 3
    col = (biqSquareIndex % 3) * 3 + smallSquareIndex % 3
    return row * 9 + col

def GetSquare(sudoku, bigSquareIndex, smallSquareIndex):
    squareIndex = TranslateFromUserIndices(bigSquareIndex, smallSquareIndex)
    return sudoku[squareIndex]

def KnockOutValueFrom(squares, value):
    newSingles = []
    for square in squares:
        if square.IsSolved():
            continue
        square.Remove(value)
        if square.IsSolved():
            newSingles.append(square)

    return newSingles   

def KnockoutValuesFromSquaresAffectedBy(square):
    squareQueue = [square]
    while len(squareQueue) > 0:
        currentSquare = squareQueue.pop(0)        
        print(f"Index {currentSquare.index} got the single value {currentSquare.Value()}. Knocking the value out.")
        squares = []
        squares.extend(GetTheOtherSquaresInSameRow(currentSquare.index, sudoku))
        squares.extend(GetTheOtherSquaresInSameCol(currentSquare.index, sudoku))
        squares.extend(GetTheOtherSquaresInTheBigSquare(currentSquare.index, sudoku))

        newSingles = KnockOutValueFrom(squares, currentSquare.Value())
        squareQueue.extend(newSingles)
    
def FindSquareHavingUniqueValue(sudoku):    
    possibleValues = {1,2,3,4,5,6,7,8,9}
    for bigSquareIndex in range(9):
        squares = GetSquaresInBigSquare(bigSquareIndex, sudoku)
        squaresWithSingleValue = filter(lambda x: len(x.possibleValues) == 1, squares)
        setValues = map(lambda square: square.Value, squaresWithSingleValue)
        unsetValues = possibleValues.difference(setValues)
        squaresWithMultipleValues = list(filter(lambda x: len(x.possibleValues) > 1, squares))
        for unsetValue in unsetValues:
            squaresHavingTheUnsetValue = list(filter(lambda x: unsetValue in x.possibleValues, squaresWithMultipleValues))
            if len(squaresHavingTheUnsetValue) == 1:
                foundSquare = squaresHavingTheUnsetValue[0]
                print(f"Square with index {foundSquare.index} has a unique value in its big square.")
                return (foundSquare, unsetValue)
    return (None, None)

def Solve(sudoku, bigSquareIndex, smallSquareIndex, value):
    square = GetSquare(sudoku, biqSquareIndex, smallSquareIndex)
    while square is not None:
        square.Set(value)
        KnockoutValuesFromSquaresAffectedBy(square)    
        (square, value) = FindSquareHavingUniqueValue(sudoku)

# Main
#==================

sudoku = CreateSudoku()
PrintSudoku(sudoku)

while True:
    userValue = input()

    if userValue == "q":
        break
    
    queue = []

    if len(userValue) == 3:
        queue.append([userValue[0], userValue[1], userValue[2]])
    
    if userValue.find(";") > -1:
        userValues = userValue.split(";")
        for uv in userValues:
            queue.append([uv[0], uv[1], uv[2]])

    while (len(queue) > 0):
        move = queue.pop(0)
        biqSquareIndex = int(move[0]) - 1
        smallSquareIndex = int(move[1]) - 1
        value = int(move[2])
        Solve(sudoku, biqSquareIndex, smallSquareIndex, value)
        PrintSudoku(sudoku)


    # Improvements:
    # 
    # Kolla igenom varje stor ruta om någon av rutorna är ensam om ett värde.
    #
    # When no more certain knockouts can be done, start trying different values out

    # Examples:
    #
    # Difficult sudoku in Dala-Demokraten 17/11 2018
    # 115;143;169;194;234;241;286;319;388;416;427;485;498;551;565;613;644;717;733;752;858;866;889;925
    #
    # Easy Dala-Demokraten 20/11 2018
    # 133;164;195;251;279;284;315;334;442;453;484;491;514;541;555;586;625;647;673;688;692;719;773;781;818;827;863;889;894;969;972;997

print("Quitting!")