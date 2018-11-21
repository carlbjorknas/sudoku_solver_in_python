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
    squareQueue = [square]
    while len(squareQueue) > 0:
        currentSquare = squareQueue.pop(0)        
        print(f"Index {currentSquare.index} got the single value {currentSquare.Value()}. Knocking the value out.")
        squares = []
        squares.extend(sudoku.GetTheOtherSquaresInSameRow(currentSquare.index))
        squares.extend(sudoku.GetTheOtherSquaresInSameCol(currentSquare.index))
        squares.extend(sudoku.GetTheOtherSquaresInTheBigSquare(currentSquare.index))

        newSingles = KnockOutValueFrom(squares, currentSquare.Value())
        squareQueue.extend(newSingles)
    
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
                print(f"Square with index {foundSquare.index} has a unique value in its big square.")
                return (foundSquare, unsetValue)
    return (None, None)

def Solve(sudoku, squareIndex, value):    
    square = sudoku.GetSquare(squareIndex)
    while square is not None:
        square.Set(value)
        KnockoutValuesFromSquaresAffectedBy(square, sudoku)    
        (square, value) = FindSquareHavingUniqueValue(sudoku)