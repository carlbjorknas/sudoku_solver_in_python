import printing, models

class Solver:
    numberGuesses = 0

    def __init__(self, sudoku, nrSquaresSolvedByBruteForce = 0):
        self.sudoku = sudoku
        self.nrSquaresSolvedByBruteForce = nrSquaresSolvedByBruteForce

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
                unsolvedSquaresHavingTheValue = [square for square in squares if not square.IsSolved() and value in square.possibleValues]
                if len(unsolvedSquaresHavingTheValue) == 1:
                    foundSquare = unsolvedSquaresHavingTheValue[0]                
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
        results = (self._BruteForceSolve(square, value) for value in square.possibleValues)
        return next((result for result in results if result[0] == True), [False, -1, Solver.numberGuesses])
            
    def _FindSquareToBruteForce(self):
        bestSquare = None
        for square in self.sudoku.squares:
            if square.IsSolved():
                continue
            if bestSquare is None or len(square.possibleValues) < len(bestSquare.possibleValues):
                bestSquare = square
        return bestSquare

    def _BruteForceSolve(self, square, value):
        Solver.numberGuesses += 1
        print(f"Bruteforcing with value {value}. Brute forcing {self.nrSquaresSolvedByBruteForce} squares, number guesses {Solver.numberGuesses}. {str(square)}")
        newSudoku = self.sudoku.Clone()
        newSquare = newSudoku.GetSquare(square.index)
        newSquare.Set(value)
        solver = Solver(newSudoku, self.nrSquaresSolvedByBruteForce + 1)
        try:
            if solver._SolveUsingKnockout([newSquare]):
                return [True, self.nrSquaresSolvedByBruteForce, Solver.numberGuesses]            
            return solver.SolveUsingBruteForce()
        except (models.SolvedSquareValueChangeException, models.SquareHasBecomeEmptyException):
            print(f"Failed bruteforcing with value {value}. {str(square)}")
            return [False, self.nrSquaresSolvedByBruteForce, Solver.numberGuesses]

    def _SolveUsingKnockout(self, solvedSquaresQueue):         
        while len(solvedSquaresQueue) > 0:            
            square = solvedSquaresQueue.pop(0)
            squaresSolvedByKnockout = self._KnockoutValuesFromSquaresAffectedBy(square)
            solvedSquaresQueue.extend(squaresSolvedByKnockout)
            printing.PrintSudoku(self.sudoku)

        return self.sudoku.IsSolved()



        