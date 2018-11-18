class Square:    
    def __init__(self):
        self.possibleValues = {1, 2, 3, 4, 5, 6, 7, 8, 9}

    def SetValue(self, value):
        self.possibleValues = {value}

    def __str__(self):
        value = ""
        if len(self.possibleValues) == 9:
            value = "1-9"
        else:
            value = "".join([str(i) for i in self.possibleValues])
        
        return value.rjust(8)

class BigSquare:
    def __init__(self):
        self.squares = [Square() for i in range(9)]

    def SetValue(self, index, value):
        self.squares[index].SetValue(value)

    def GetStringForRow(self, i):
        base = i*3
        return str(self.squares[base]) + ", " + str(self.squares[base+1]) + ", " + str(self.squares[base+2])


class Board:
    def __init__(self):
        self.squares = [BigSquare() for i in range(9)]

    def SetValue(self, bigIndex, smallIndex, value):
        self.squares[bigIndex].SetValue(smallIndex, value)

    def __str__(self):
        horizontalDelimiter = "-" * 94
        rows = list()
        rows.append(horizontalDelimiter)            
        for bigSquareRowIndex in range(3):
            bigSquareBaseIndex = bigSquareRowIndex * 3
            for rowIndex in range (3):                
                left = self.squares[bigSquareBaseIndex].GetStringForRow(rowIndex)
                middle = self.squares[bigSquareBaseIndex+1].GetStringForRow(rowIndex)
                right = self.squares[bigSquareBaseIndex+2].GetStringForRow(rowIndex)
                rows.append(f"| {left} | {middle} | {right} |")
            rows.append(horizontalDelimiter)            
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

    board.SetValue(biqSquareIndex-1, squareIndex-1, value)
    print(board)

print("Quitting!")

