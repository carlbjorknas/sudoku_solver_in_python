class Helper:
    def GetOtherIndicesOnSameRowAs(self, index):
        indices = self.GetAllIndicesOnSameRowAs(index)
        indices.remove(index)
        return indices

    def GetAllIndicesOnSameRowAs(self, index):
        rowIndex = index // 3
        baseIndex = rowIndex * 3
        return {baseIndex, baseIndex+1, baseIndex+2}

    def GetOtherIndicesInSameColumnAs(self, index):
        indices = self.GetAllIndicesInSameColumnAs(index)
        indices.remove(index)
        return indices

    def GetAllIndicesInSameColumnAs(self, index):
        colIndex = index % 3
        return {colIndex, colIndex + 3, colIndex + 6}

class Square:    
    def __init__(self):
        self.possibleValues = {1, 2, 3, 4, 5, 6, 7, 8, 9}

    def SetValue(self, value):
        self.possibleValues = {value}

    def Knockout(self, value):
        self.possibleValues.discard(value)

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
        for square in self._GetAllSquaresBut(index):
            square.Knockout(value)

    def KnockOutOnRow(self, index, value):  
        indices = Helper().GetAllIndicesOnSameRowAs(index)
        for index in indices:
            self.squares[index].Knockout(value)

    def KnockOutInColumn(self, index, value):
        indices = Helper().GetAllIndicesInSameColumnAs(index)
        for index in indices:
            self.squares[index].Knockout(value)       

    def _GetAllSquaresBut(self, indexToExclude):
        indices = filter(lambda x: x != indexToExclude, range(9))
        return [self.squares[i] for i in indices]

    def GetStringForRow(self, i):
        base = i*3
        return str(self.squares[base]) + ", " + str(self.squares[base+1]) + ", " + str(self.squares[base+2])


class Board:
    def __init__(self):
        self.squares = [BigSquare() for i in range(9)]

    def SetValue(self, bigIndex, smallIndex, value):
        self.squares[bigIndex].SetValue(smallIndex, value)
        othersOnRow = self._GetOtherSquaresOnRow(bigIndex)

        for otherOnRow in othersOnRow:
            otherOnRow.KnockOutOnRow(smallIndex, value)

        othersInColumn = self._GetOtherSquaresInColumn(bigIndex)
        for otherInColumn in othersInColumn:
            otherInColumn.KnockOutInColumn(smallIndex, value)   

    def _GetOtherSquaresOnRow(self, index):
        indices = Helper().GetOtherIndicesOnSameRowAs(index)
        return [self.squares[i] for i in indices]

    def _GetOtherSquaresInColumn(self, index):
        indices = Helper().GetOtherIndicesInSameColumnAs(index)
        return [self.squares[i] for i in indices]

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

    # Förbättringar:
    # 1.
    # När bortslagning görs och en liten ruta bara får ett värde kvar,
    # kör en bortslagning av den med.
    # 2.
    # Kolla igenom varje stor ruta om någon av rutorna är ensam om ett värde.

print("Quitting!")

