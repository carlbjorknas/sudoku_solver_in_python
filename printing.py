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
        row = sudoku.GetRow(rowIndex)
        rowStr = GetSudokuRowString(row)
        rows.append(rowStr)
        if rowIndex > 0 and rowIndex % 3 == 2:
            rows.append(horizontalDelimiter)
    print("\n".join(rows))   