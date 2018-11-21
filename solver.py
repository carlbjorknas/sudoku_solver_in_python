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
        print(f"Index {square.index} got the single value {square.Value()}. Knocking the value out.")
        squares = []
        squares.extend(self.sudoku.GetTheOtherSquaresInSameRow(square.index))
        squares.extend(self.sudoku.GetTheOtherSquaresInSameCol(square.index))
        squares.extend(self.sudoku.GetTheOtherSquaresInTheBigSquare(square.index))

        newSingles = self._KnockOutValueFrom(squares, square.Value())
        return newSingles

    @staticmethod
    def _FindSquareHavingUniqueValueUsing(squareSelector):
        possibleValues = {1,2,3,4,5,6,7,8,9}
        for index in range(9):
            squares = squareSelector(index)
            solvedValues = [square.Value() for square in squares if square.IsSolved()]
            unsolvedValues = possibleValues.difference(solvedValues)
            for unsolvedValue in unsolvedValues:
                squaresHavingTheUnsolvedValue = [square for square in squares if unsolvedValue in square.possibleValues]
                if len(squaresHavingTheUnsolvedValue) == 1:
                    foundSquare = squaresHavingTheUnsolvedValue[0]                
                    return (foundSquare, unsolvedValue)
        return None

    def _FindSquareHavingUniqueValue(self): 
        squareSelectors = [
            ("big square", lambda bigSquareIndex: self.sudoku.GetSquaresInBigSquare(bigSquareIndex)),
            ("row", lambda rowIndex: self.sudoku.GetRow(rowIndex)),
            ("column", lambda colIndex: self.sudoku.GetColumn(colIndex))
        ]
        for (description, squareSeletor) in squareSelectors:  
            result = self._FindSquareHavingUniqueValueUsing(squareSeletor)
            if result is None:
                continue
            (square, value) = result
            print(f"Square with index {square.index} has a unique value {value} in its {description}.")
            return result

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