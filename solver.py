import printing

class Solver:

    def __init__(self, sudoku, level = 1, numberGuesses = 0):
        self.sudoku = sudoku
        self.level = level
        self.numberGuesses = numberGuesses

    @staticmethod
    def _KnockOutValueFrom(squares, value):
        newSingles = []
        for square in squares:
            solvedBefore = square.IsSolved()
            square.Remove(value)
            if square.IsSolved() and not solvedBefore:
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

    def SolveUsingKnockout(self):
        solvedSquaresQueue = self.sudoku.GetSolvedSquares() 
        return self._SolveUsingKnockout(solvedSquaresQueue)

    def SolveByFindingUniqueValues(self):
        while True:
            result = self._FindSquareHavingUniqueValue()
            if result is None:
                return False
            (square, value) = result
            square.Set(value)
            solved = self._SolveUsingKnockout([square])
            if solved:
                return True
        return False  

    def SolveUsingBruteForce(self):
        square = self._FindSquareToBruteForce()
        return any((self._BruteForceSolve(square, value) for value in square.possibleValues))
            
    def _FindSquareToBruteForce(self):
        bestSquare = None
        for square in self.sudoku.squares:
            if square.IsSolved():
                continue
            if bestSquare is None or len(square.possibleValues) < len(bestSquare.possibleValues):
                bestSquare = square
        return bestSquare

    def _BruteForceSolve(self, square, value):
        self.numberGuesses += 1
        print(f"Bruteforcing with value {value}, level {self.level}, number guesses {self.numberGuesses}. {str(square)}")
        newSudoku = self.sudoku.Clone()
        newSquare = newSudoku.GetSquare(square.index)
        newSquare.Set(value)
        solver = Solver(newSudoku, self.level+1, self.numberGuesses)
        try:
            return solver._SolveUsingKnockout([newSquare]) or solver.SolveByFindingUniqueValues() or solver.SolveUsingBruteForce()
        except:
            print(f"Failed bruteforcing with value {value}. {str(square)}")
            return False

    def _SolveUsingKnockout(self, solvedSquaresQueue):         
        while len(solvedSquaresQueue) > 0:            
            square = solvedSquaresQueue.pop(0)
            squaresSolvedByKnockout = self._KnockoutValuesFromSquaresAffectedBy(square)
            solvedSquaresQueue.extend(squaresSolvedByKnockout)
            printing.PrintSudoku(self.sudoku)

        return self.sudoku.IsSolved()



        