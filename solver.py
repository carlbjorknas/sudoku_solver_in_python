class Square:
    possibleValues = {1, 2, 3, 4, 5, 6, 7, 8, 9}

    def __str__(self):
        if len(self.possibleValues) == 9:
            return "1-9"
        else:
            str = ""
            [str + val for val in self.possibleValues]
            return str

class BigSquare:
    squares = [Square() for i in range(9)]

    def GetStringForRow(self, i):
        base = i*3
        return str(self.squares[base]) + ", " + str(self.squares[base+1]) + ", " + str(self.squares[base+2])


class Board:
    squares = [BigSquare() for i in range(9)]

    def __str__(self):
        rows = list()
        rows.append("-------------------------------------------------")            
        for bigSquareRowIndex in range(3):
            bigSquareBaseIndex = bigSquareRowIndex * 3
            for rowIndex in range (3):                
                left = self.squares[bigSquareBaseIndex].GetStringForRow(rowIndex)
                middle = self.squares[bigSquareBaseIndex+1].GetStringForRow(rowIndex)
                right = self.squares[bigSquareBaseIndex+2].GetStringForRow(rowIndex)
                rows.append(f"| {left} | {middle} | {right} |")
            rows.append("-------------------------------------------------")            
        rowBreak = "\n"
        return rowBreak.join(rows)


board = Board()
print(board)

while True:
    userValue = input()

    if userValue == "q":
        break
    
    biqSquareIndex = int(userValue[0])
    squareIndex = int(userValue[1])
    value = int(userValue[2])

print("Quitting!")

