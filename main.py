import models, printing, solver

def TranslateFromUserIndices(bigSquareIndex, smallSquareIndex):
    bsIndex = int(bigSquareIndex) - 1
    ssIndex = int(smallSquareIndex) - 1
    row = (bsIndex // 3) * 3 + ssIndex // 3
    col = (bsIndex % 3) * 3 + ssIndex % 3
    return row * 9 + col

sudoku = models.Sudoku()
theSolver = solver.Solver(sudoku)
printing.PrintSudoku(sudoku)
print("The board above shows the possible values for each square.")
print("Add the known values. Use the the format [big square index][small square index][value].")
print("Top left square has index 1, top middle square has index 2, top right square has index 3 and so on.")
print("To set the value 9 in the center of the top left big square, write 159 and press enter.")
print("Multiple values can be set at once by using ';' as separator, like this 159;225;345")
print("")
print("When all values are set, you have to begin the solving by using the knockout method.")
print("Then you can follow that up with any of the other two.")

while True:
    userValue = input()

    if userValue == "q":
        break
    
    if userValue == "k":
        solved = theSolver.SolveUsingKnockout()
        print(f"This sudoku is {'solved!:D' if solved else 'not solved... :_('}")
        if solved:
            break
    elif userValue == "u":
        solved = theSolver.SolveByFindingUniqueValues()
        print(f"This sudoku is {'solved!:D' if solved else 'not solved... :_('}")
        if solved:
            break 
    elif userValue == "b":
        solved = theSolver.SolveUsingBruteForce()
        print(f"This sudoku is {'solved!:D' if solved else 'not solved... :_('}. Used {solver.Solver.numberGuesses} guesses.")
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

    print("q:quit, k:knockout, u:findUnique, b:bruteforce")

    # Improvements:
    #
    # Write to log file

    # Examples:
    #
    # Difficult sudoku in Dala-Demokraten 17/11 2018 
    # Solved using knockout and unique value finder
    # 115;143;169;194;234;241;286;319;388;416;427;485;498;551;565;613;644;717;733;752;858;866;889;925
    #
    # Medium Dala-Demokraten 23/11 2018 
    # Solved using knockout, unique value finder and brute force
    # 123;157;188;218;221;245;274;286;314;361;382;399;446;478;495;541;565;589;722;749;825;842;854;866;891;934;941;989
    #
    # Easy Dala-Demokraten 20/11 2018 
    # Solved using knockout only
    # 133;164;195;251;279;284;315;334;442;453;484;491;514;541;555;586;625;647;673;688;692;719;773;781;818;827;863;889;894;969;972;997

print("Quitting!")