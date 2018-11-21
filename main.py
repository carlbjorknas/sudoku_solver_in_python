import models, printing, solver

def TranslateFromUserIndices(bigSquareIndex, smallSquareIndex):
    bsIndex = int(bigSquareIndex) - 1
    ssIndex = int(smallSquareIndex) - 1
    row = (bsIndex // 3) * 3 + ssIndex // 3
    col = (bsIndex % 3) * 3 + ssIndex % 3
    return row * 9 + col

sudoku = models.Sudoku()
printing.PrintSudoku(sudoku)

while True:
    userValue = input()

    if userValue == "q":
        break
    
    if userValue == "s":
        solved = solver.Solver(sudoku).Solve()
        print(f"This sudoku is {'solved!:D' if solved else 'not solved... :_('}")
        if solved:
            break
    else:    
        # Assume there is a single command or a list of commands separated by ";"
        valuesToSet = [[uv[0], uv[1], uv[2]] for uv in userValue.split(";")]

        for valueToSet in valuesToSet:
            (biqSquareIndex, smallSquareIndex, value) = valueToSet
            squareIndex = TranslateFromUserIndices(biqSquareIndex, smallSquareIndex)
            square = sudoku.GetSquare(squareIndex)
            square.Set(int(value))
        printing.PrintSudoku(sudoku)            

    # Improvements:
    #
    # When no more certain knockouts can be done, start trying different values out

    # Examples:
    #
    # Difficult sudoku in Dala-Demokraten 17/11 2018
    # 115;143;169;194;234;241;286;319;388;416;427;485;498;551;565;613;644;717;733;752;858;866;889;925
    #
    # Easy Dala-Demokraten 20/11 2018
    # 133;164;195;251;279;284;315;334;442;453;484;491;514;541;555;586;625;647;673;688;692;719;773;781;818;827;863;889;894;969;972;997

print("Quitting!")