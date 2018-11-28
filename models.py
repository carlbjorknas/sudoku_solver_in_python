class SolvedSquareValueChangeException(Exception):
    pass

class SquareHasBecomeEmptyException(Exception):
    pass

class Square:
    def __init__(self, index):
        self.possibleValues = [1,2,3,4,5,6,7,8,9]
        self.index = index

    def Set(self, value):
        if self.IsSolved() and self.Value() != value:
            raise SolvedSquareValueChangeException()
        self.possibleValues = [value]

    def Remove(self, value):
        if value in self.possibleValues:
            self.possibleValues.remove(value)
            if len(self.possibleValues) == 0:
                raise SquareHasBecomeEmptyException

    def Value(self):
        if not self.IsSolved():
            raise Exception("Cannot get the value if the square isn't solved.")
        return self.possibleValues[0]
    
    def IsSolved(self):
        return len(self.possibleValues) == 1

    def __str__(self):
        bigSquareUserIndex = self.GetBigSquareIndex() + 1
        smallSquareUserIndex = self._GetSmallSquareIndex() + 1
        valueString = ','.join([str(value) for value in self.possibleValues])
        return f"Index:{bigSquareUserIndex},{smallSquareUserIndex} Value(s):{valueString}"

    def GetBigSquareIndex(self):        
        rowIndex = self.index // (9 * 3)
        colIndex = (self.index // 3) % 3
        return rowIndex * 3 + colIndex

    def _GetSmallSquareIndex(self):
        row = (self.index % 27) // 9
        col = self.index % 3
        return row * 3 + col


class Sudoku:
    def __init__(self):
        self.squares = [Square(i) for i in range(81)]
    
    def Clone(self):
        newSudoku = Sudoku()
        newSudoku.squares = []
        for square in self.squares:
            newSquare = Square(square.index)
            newSquare.possibleValues = list(square.possibleValues)
            newSudoku.squares.append(newSquare)
        return newSudoku

    def IsSolved(self):
        return all((square.IsSolved() for square in self.squares))

    def GetSquare(self, squareIndex):
        return self.squares[squareIndex]

    def GetSolvedSquares(self):
        return [square for square in self.squares if square.IsSolved()]        

    def GetRow(self, rowIndex):
        start = rowIndex * 9
        stop = start + 9
        return self.squares[slice(start, stop)]

    def GetTheOtherSquaresInSameRow(self, squareIndex):
        rowIndex = squareIndex // 9
        row = self.GetRow(rowIndex)
        return  filter(lambda x: x.index != squareIndex, row)

    def GetColumn(self, colIndex):
        return self.squares[slice(colIndex, None, 9)]

    def GetTheOtherSquaresInSameCol(self, squareIndex):
        colIndex = squareIndex % 9
        col = self.GetColumn(colIndex)
        return filter(lambda x: x.index != squareIndex, col)

    @staticmethod
    def _GetIndicesInBigSquare(bigSquareIndex):
        row = bigSquareIndex // 3
        col = bigSquareIndex % 3
        startIndex = row * 27 + col * 3
        return {
            startIndex, startIndex + 1, startIndex + 2,
            startIndex + 9, startIndex + 10, startIndex + 11,
            startIndex + 18, startIndex + 19, startIndex + 20
            }

    def GetSquaresInBigSquare(self, bigSquareIndex):
        indices = self._GetIndicesInBigSquare(bigSquareIndex)
        return [self.squares[i] for i in indices]

    def GetTheOtherSquaresInTheBigSquare(self, square):
        bigSquareIndex = square.GetBigSquareIndex()
        squares = self.GetSquaresInBigSquare(bigSquareIndex)
        return filter(lambda x: x.index != square.index, squares)