# Helpers
#===============

def CreateSudoku():
    return [{1,2,3,4,5,6,7,8,9} for i in range(81)]

def GetRow(rowIndex, sudoku):
    start = rowIndex * 9
    stop = start + 9
    return sudoku[slice(start, stop)]

def GetTheOtherSquaresInSameRow(squareIndex, sudoku):
    rowIndex = squareIndex // 9
    colIndex = squareIndex % 9
    row = GetRow(rowIndex, sudoku)
    del row[colIndex]
    return row

def GetTheOtherSquaresInSameCol(squareIndex, sudoku):
    colIndex = squareIndex % 9
    rowIndex = squareIndex // 9
    col = sudoku[slice(colIndex, None, 9)]
    del col[rowIndex]
    return col

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
    squareStrings = [GetSquareString(square) for square in bigSquareRow]
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
    for square in squares:
        square.discard(value)    

def SetValue(sudoku, bigSquareIndex, smallSquareIndex, value):
    squareIndex = TranslateFromUserIndices(bigSquareIndex, smallSquareIndex)
    sudoku[squareIndex] = {value}

    squaresInRow = GetTheOtherSquaresInSameRow(squareIndex, sudoku)
    KnockOutValueFrom(squaresInRow, value)

    squaresInColumn = GetTheOtherSquaresInSameCol(squareIndex, sudoku)
    KnockOutValueFrom(squaresInColumn, value)

    squaresInBigSquare = GetTheOtherSquaresInTheBigSquare(squareIndex, sudoku)
    KnockOutValueFrom(squaresInBigSquare, value)
    
# Main
#==================

sudoku = CreateSudoku()
PrintSudoku(sudoku)

while True:
    userValue = input()

    if userValue == "q":
        break
    
    biqSquareIndex = int(userValue[0])-1
    smallSquareIndex = int(userValue[1])-1
    value = int(userValue[2])

    SetValue(sudoku, biqSquareIndex, smallSquareIndex, value)
    PrintSudoku(sudoku)

    # Förbättringar:
    # 1.
    # När bortslagning görs och en liten ruta bara får ett värde kvar,
    # kör en bortslagning av den med.
    # 2.
    # Kolla igenom varje stor ruta om någon av rutorna är ensam om ett värde.

print("Quitting!")


# class Helper:
#     def GetOtherIndicesOnSameRowAs(self, index):
#         indices = self.GetAllIndicesOnSameRowAs(index)
#         indices.remove(index)
#         return indices

#     def GetAllIndicesOnSameRowAs(self, index):
#         rowIndex = index // 3
#         baseIndex = rowIndex * 3
#         return {baseIndex, baseIndex+1, baseIndex+2}

#     def GetOtherIndicesInSameColumnAs(self, index):
#         indices = self.GetAllIndicesInSameColumnAs(index)
#         indices.remove(index)
#         return indices

#     def GetAllIndicesInSameColumnAs(self, index):
#         colIndex = index % 3
#         return {colIndex, colIndex + 3, colIndex + 6}

# class Square:    
#     def __init__(self):
#         self.possibleValues = {1, 2, 3, 4, 5, 6, 7, 8, 9}

#     def SetValue(self, value):
#         self.possibleValues = {value}

#     def Knockout(self, value):
#         self.possibleValues.discard(value)

#     def __str__(self):
#         value = ""
#         if len(self.possibleValues) == 9:
#             value = "1-9"
#         else:
#             value = "".join([str(i) for i in self.possibleValues])
        
#         return value.rjust(8)

# class BigSquare:
#     def __init__(self):
#         self.squares = [Square() for i in range(9)]

#     def SetValue(self, index, value):
#         self.squares[index].SetValue(value)
#         for square in self._GetAllSquaresBut(index):
#             square.Knockout(value)

#     def KnockOutOnRow(self, index, value):  
#         indices = Helper().GetAllIndicesOnSameRowAs(index)
#         for index in indices:
#             self.squares[index].Knockout(value)

#     def KnockOutInColumn(self, index, value):
#         indices = Helper().GetAllIndicesInSameColumnAs(index)
#         for index in indices:
#             self.squares[index].Knockout(value)       

#     def _GetAllSquaresBut(self, indexToExclude):
#         indices = filter(lambda x: x != indexToExclude, range(9))
#         return [self.squares[i] for i in indices]

#     def GetStringForRow(self, i):
#         base = i*3
#         return str(self.squares[base]) + ", " + str(self.squares[base+1]) + ", " + str(self.squares[base+2])


# class Board:
#     def __init__(self):
#         self.squares = [BigSquare() for i in range(9)]

#     def SetValue(self, bigIndex, smallIndex, value):
#         self.squares[bigIndex].SetValue(smallIndex, value)
#         othersOnRow = self._GetOtherSquaresOnRow(bigIndex)

#         for otherOnRow in othersOnRow:
#             otherOnRow.KnockOutOnRow(smallIndex, value)

#         othersInColumn = self._GetOtherSquaresInColumn(bigIndex)
#         for otherInColumn in othersInColumn:
#             otherInColumn.KnockOutInColumn(smallIndex, value)   

#     def _GetOtherSquaresOnRow(self, index):
#         indices = Helper().GetOtherIndicesOnSameRowAs(index)
#         return [self.squares[i] for i in indices]

#     def _GetOtherSquaresInColumn(self, index):
#         indices = Helper().GetOtherIndicesInSameColumnAs(index)
#         return [self.squares[i] for i in indices]

#     def __str__(self):
#         horizontalDelimiter = "-" * 94
#         rows = list()
#         rows.append(horizontalDelimiter)            
#         for bigSquareRowIndex in range(3):
#             bigSquareBaseIndex = bigSquareRowIndex * 3
#             for rowIndex in range (3):                
#                 left = self.squares[bigSquareBaseIndex].GetStringForRow(rowIndex)
#                 middle = self.squares[bigSquareBaseIndex+1].GetStringForRow(rowIndex)
#                 right = self.squares[bigSquareBaseIndex+2].GetStringForRow(rowIndex)
#                 rows.append(f"| {left} | {middle} | {right} |")
#             rows.append(horizontalDelimiter)            
#         rowBreak = "\n"
#         return rowBreak.join(rows)


# board = Board()


