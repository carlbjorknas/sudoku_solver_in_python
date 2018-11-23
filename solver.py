import printing

class Solver:

    def __init__(self, sudoku):
        self.sudoku = sudoku

    @staticmethod
    def _KnockOutValueFrom(squares, value):
        newSingles = []
        for square in squares:
            if square.IsSolved():
                continue
            square.Remove(value)
            if square.IsSolved():
                newSingles.append(square)

        return newSingles   

    def _KnockoutValuesFromSquaresAffectedBy(self, square):      
        print(f"Square has been solved. Knocking the value out from affected squares. {str(square)}")
        squares = []
        squares.extend(self.sudoku.GetTheOtherSquaresInSameRow(square.index))
        squares.extend(self.sudoku.GetTheOtherSquaresInSameCol(square.index))
        squares.extend(self.sudoku.GetTheOtherSquaresInTheBigSquare(square))

        newSingles = self._KnockOutValueFrom(squares, square.Value())
        return newSingles

    def _FindSquareHavingUniqueValue(self): 
        for biqSquareIndex in range(9):
            squares = self.sudoku.GetSquaresInBigSquare(biqSquareIndex)
            for value in {1,2,3,4,5,6,7,8,9}:
                usolvedSquaresHavingTheValue = [square for square in squares if not square.IsSolved() and value in square.possibleValues]
                if len(usolvedSquaresHavingTheValue) == 1:
                    foundSquare = usolvedSquaresHavingTheValue[0]                
                    print(f"Square with has a unique value {value} in its big square. {str(foundSquare)}")
                    return (foundSquare, value)
        return None

    def Solve(self):
        solvedSquaresQueue = self.sudoku.GetSolvedSquares()  
        while len(solvedSquaresQueue) > 0:
            square = solvedSquaresQueue.pop(0)
            squaresSolvedByKnockout = self._KnockoutValuesFromSquaresAffectedBy(square)
            solvedSquaresQueue.extend(squaresSolvedByKnockout)
            printing.PrintSudoku(self.sudoku)
            if len(solvedSquaresQueue) == 0:
                if self.sudoku.IsSolved():
                    return True
                result = self._FindSquareHavingUniqueValue()
                if result is not None:
                    (square, value) = result
                    square.Set(value)
                    solvedSquaresQueue = [square]
                    continue

        return False