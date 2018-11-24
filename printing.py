import datetime
from time import strftime

# class Logger:
#     def _init__(self):
#         filename = strftime("%Y%m%d %H-%M-%S", datetime.datetime.now()) + ".log"
#         self.file = open("")

def GetSquareString(possibleSquareValues, useQuestionMarks):
    if useQuestionMarks:
        val = (str(possibleSquareValues[0]) if len(possibleSquareValues) == 1 else ".")                
    elif len(possibleSquareValues) == 9:
        val = "1-9" 
    else: 
        val = "".join([str(i) for i in possibleSquareValues])
    return val.rjust(8)

def GetSudokuBigSquareRowString(bigSquareRow, useQuestionMarks):
    squareStrings = [GetSquareString(square.possibleValues, useQuestionMarks) for square in bigSquareRow]
    return " ".join(squareStrings)

def GetSudokuRowString(row, useQuestionMarks):
    rowParts = [row[i:i+3] for i in range(0, len(row), 3)]
    left = GetSudokuBigSquareRowString(rowParts[0], useQuestionMarks)
    middle = GetSudokuBigSquareRowString(rowParts[1], useQuestionMarks)
    right = GetSudokuBigSquareRowString(rowParts[2], useQuestionMarks)
    return f"| {left} | {middle} | {right} |"

def PrintSudoku(sudoku, useQuestionMarks=False):
    horizontalDelimiter = "-" * 88

    rows = list()
    rows.append(horizontalDelimiter)
    for rowIndex in range(9):
        row = sudoku.GetRow(rowIndex)
        rowStr = GetSudokuRowString(row, useQuestionMarks)
        rows.append(rowStr)
        if rowIndex > 0 and rowIndex % 3 == 2:
            rows.append(horizontalDelimiter)
    print("\n".join(rows))   