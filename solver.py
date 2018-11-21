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

def _FindSquareHavingUniqueValue(squareSelector):
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

def FindSquareHavingUniqueValue(sudoku): 
    squareSelectors = [
        ("big square", lambda bigSquareIndex: sudoku.GetSquaresInBigSquare(bigSquareIndex)),
        ("row", lambda rowIndex: sudoku.GetRow(rowIndex)),
        ("column", lambda colIndex: sudoku.GetColumn(colIndex))
    ]
    for (description, squareSeletor) in squareSelectors:  
        result = _FindSquareHavingUniqueValue(squareSeletor)
        if result is None:
            continue
        (square, value) = result
        print(f"Square with index {square.index} has a unique value {value} in its {description}.")
        return result

    return None

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
            result = FindSquareHavingUniqueValue(sudoku)
            if result is not None:
                (square, value) = result
                square.Set(value)
                solvedSquaresQueue = [square]
                continue

    return False