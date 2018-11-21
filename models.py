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

class Sudoku:
    def __init__(self):
        self.squares = [Square(i) for i in range(81)]

    def GetSquare(self, squareIndex):
        return self.squares[squareIndex]

    def GetRow(self, rowIndex):
        start = rowIndex * 9
        stop = start + 9
        return self.squares[slice(start, stop)]

    def GetTheOtherSquaresInSameRow(self, squareIndex):
        rowIndex = squareIndex // 9
        row = self.GetRow(rowIndex)
        return  filter(lambda x: x.index != squareIndex, row)

    def GetTheOtherSquaresInSameCol(self, squareIndex):
        colIndex = squareIndex % 9
        col = self.squares[slice(colIndex, None, 9)]
        return filter(lambda x: x.index != squareIndex, col)

    @staticmethod
    def _GetBigSquareIndex(squareIndex):        
        rowIndex = squareIndex // (9 * 3)
        colIndex = (squareIndex // 3) % 3
        return rowIndex * 3 + colIndex

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

    def GetTheOtherSquaresInTheBigSquare(self, squareIndex):
        bigSquareIndex = self._GetBigSquareIndex(squareIndex)
        squares = self.GetSquaresInBigSquare(bigSquareIndex)
        return filter(lambda x: x.index != squareIndex, squares)