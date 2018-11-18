class Square:
    def __init__(self, index):
        self.possibleValues = {1,2,3,4,5,6,7,8,9}
        self.index = index

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

def GetTheOtherSquaresInTheBigSquare(squareIndex, sudoku):
    bigSquareIndex = GetBigSquareIndex(squareIndex)
    indices = GetIndicesInBigSquare(bigSquareIndex)
    indices.remove(squareIndex)    
    return [sudoku[i] for i in indices]

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

def KnockOutValueFrom(squares, value):
    newSingles = []
    for square in squares:
        lenBefore = len(square.possibleValues)
        square.possibleValues.discard(value)
        lenAfter = len(square.possibleValues) 
        if (lenAfter == 0):
            raise Exception("All values has been knocked out!")
        if lenAfter == 1 and lenBefore == 2:
            newSingles.append(square)

    return newSingles            

def SetValue(sudoku, bigSquareIndex, smallSquareIndex, value):
    squareIndex = TranslateFromUserIndices(bigSquareIndex, smallSquareIndex)
    
    if len(sudoku[squareIndex].possibleValues) == 1:
        raise Exception("Resetting a single value!")

    sudoku[squareIndex].possibleValues = {value}
    queue = [sudoku[squareIndex]]

    while len(queue) > 0:
        currentSquare = queue.pop(0)
        currentValue = next(iter(currentSquare.possibleValues)) # possibleValues is a set and cannot be indexed
        print(f"Index {currentSquare.index} got the single value {currentValue}. Knocking the value out.")
        squares = []
        squares.extend(GetTheOtherSquaresInSameRow(currentSquare.index, sudoku))
        squares.extend(GetTheOtherSquaresInSameCol(currentSquare.index, sudoku))
        squares.extend(GetTheOtherSquaresInTheBigSquare(currentSquare.index, sudoku))

        newSingles = KnockOutValueFrom(squares, currentValue)
        queue.extend(newSingles)
    
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
        SetValue(sudoku, biqSquareIndex, smallSquareIndex, value)
        PrintSudoku(sudoku)


    # Förbättringar:
    # 
    # Kolla igenom varje stor ruta om någon av rutorna är ensam om ett värde.

    # Exempel
    #
    # Svårt sudoku Dala-Demokraten 17/11 2018
    # 115;143;169;194;234;241;286;319;388;416;427;485;498;551;565;613;644;717;733;752;858;866;889;925

print("Quitting!")