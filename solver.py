import printing

def KnockOutValueFrom(squares, value):
    newSingles = []
    for square in squares:
        if square.IsSolved():
            continue
        square.Remove(value)
        if square.IsSolved():
            newSingles.append(square)

    return newSingles   

def KnockoutValuesFromSquaresAffectedBy(square, sudoku):      
    print(f"Index {square.index} got the single value {square.Value()}. Knocking the value out.")
    squares = []
    squares.extend(sudoku.GetTheOtherSquaresInSameRow(square.index))
    squares.extend(sudoku.GetTheOtherSquaresInSameCol(square.index))
    squares.extend(sudoku.GetTheOtherSquaresInTheBigSquare(square.index))

    newSingles = KnockOutValueFrom(squares, square.Value())
    return newSingles
    
def FindSquareHavingUniqueValue(sudoku):    
    possibleValues = {1,2,3,4,5,6,7,8,9}
    for bigSquareIndex in range(9):
        squares = sudoku.GetSquaresInBigSquare(bigSquareIndex)
        squaresWithSingleValue = filter(lambda x: len(x.possibleValues) == 1, squares)
        setValues = map(lambda square: square.Value, squaresWithSingleValue)
        unsetValues = possibleValues.difference(setValues)
        squaresWithMultipleValues = list(filter(lambda x: len(x.possibleValues) > 1, squares))
        for unsetValue in unsetValues:
            squaresHavingTheUnsetValue = list(filter(lambda x: unsetValue in x.possibleValues, squaresWithMultipleValues))
            if len(squaresHavingTheUnsetValue) == 1:
                foundSquare = squaresHavingTheUnsetValue[0]
                print(f"Square with index {foundSquare.index} has a unique value {unsetValue} in its big square.")
                return (foundSquare, unsetValue)
    return (None, None)

def Solve(sudoku):
    solvedSquaresQueue = sudoku.GetSolvedSquares()  
    while len(solvedSquaresQueue) > 0:
        square = solvedSquaresQueue.pop(0)
        squaresSolvedByKnockout = KnockoutValuesFromSquaresAffectedBy(square, sudoku)
        solvedSquaresQueue.extend(squaresSolvedByKnockout)
        printing.PrintSudoku(sudoku)
        if len(solvedSquaresQueue) == 0:
            if sudoku.IsSolved():
                return True
            (square, value) = FindSquareHavingUniqueValue(sudoku)
            if square is not None:
                square.Set(value)
                solvedSquaresQueue = [square]
                continue

    return False