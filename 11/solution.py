import os
from copy import deepcopy

def part1(seatGrid):
  numRows = len(seatGrid)
  numCols = len(seatGrid[0])

  numberOfMoves = None

  while numberOfMoves != 0:
    newSeatGrid = deepcopy(seatGrid)
    numberOfMoves = 0

    for rowIdx in range(numRows):
      for colIdx in range(numCols):
        seat = seatGrid[rowIdx][colIdx]

        seatTop = None
        if rowIdx - 1 >= 0:
          seatTop = seatGrid[rowIdx - 1][colIdx]
        seatBottom = None
        if rowIdx + 1 < numCols:
          seatBottom = seatGrid[rowIdx + 1][colIdx]

        seatLeft = None
        seatTopLeft = None
        seatBottomLeft = None
        if colIdx - 1 >= 0:
          seatLeft = seatGrid[rowIdx][colIdx - 1]
          if rowIdx - 1 >= 0:
            seatTopLeft = seatGrid[rowIdx - 1][colIdx - 1]
          if rowIdx + 1 < numCols:
            seatBottomLeft = seatGrid[rowIdx + 1][colIdx - 1]

        seatRight = None
        seatTopRight = None
        seatBottomRight = None
        if colIdx + 1 < numCols:
          seatRight = seatGrid[rowIdx][colIdx + 1]
          if rowIdx - 1 >= 0:
            seatTopRight = seatGrid[rowIdx - 1][colIdx + 1]
          if rowIdx + 1 < numCols:
            seatBottomRight = seatGrid[rowIdx + 1][colIdx + 1]

        occupiedAround = [seatTop, seatBottom, seatLeft, seatTopLeft, seatBottomLeft, seatRight, seatTopRight, seatBottomRight].count('#')

        if seat == "L" and occupiedAround == 0:
          newSeatGrid[rowIdx][colIdx] = "#"
          numberOfMoves += 1
        elif seat == "#" and occupiedAround >= 4:
          newSeatGrid[rowIdx][colIdx] = "L"
          numberOfMoves += 1

    seatGrid = newSeatGrid
    
  numOccupied = 0
  for rowIdx in range(numRows):
    for colIdx in range(numCols):
      if seatGrid[rowIdx][colIdx] == "#":
        numOccupied += 1
      
  print(f"Part 1 - Solution: {numOccupied}")


def part2(seatGrid):
  numRows = len(seatGrid)
  numCols = len(seatGrid[0])

  numberOfMoves = None

  while numberOfMoves != 0:
    newSeatGrid = deepcopy(seatGrid)
    numberOfMoves = 0

    for rowIdx in range(numRows):
      for colIdx in range(numCols):
        seat = seatGrid[rowIdx][colIdx]

        seatTop = None
        topIdx = rowIdx - 1
        while topIdx >= 0 and seatTop == None:
          if seatGrid[topIdx][colIdx] == ".":
            topIdx -= 1
          else:
            seatTop = seatGrid[topIdx][colIdx]

        seatBottom = None
        bottomIdx = rowIdx + 1
        while bottomIdx < numRows and seatBottom == None:
          if seatGrid[bottomIdx][colIdx] == ".":
            bottomIdx += 1
          else:
            seatBottom = seatGrid[bottomIdx][colIdx]

        seatLeft = None
        leftIdx = colIdx - 1
        while leftIdx >= 0 and seatLeft == None:
          if seatGrid[rowIdx][leftIdx] == ".":
            leftIdx -= 1
          else:
            seatLeft = seatGrid[rowIdx][leftIdx]

        seatRight = None
        rightIdx = colIdx + 1
        while rightIdx < numCols and seatRight == None:
          if seatGrid[rowIdx][rightIdx] == ".":
            rightIdx += 1
          else:
            seatRight = seatGrid[rowIdx][rightIdx]

        seatTopLeft = None
        topIdx = rowIdx - 1
        leftIdx = colIdx - 1
        while topIdx >= 0 and leftIdx >= 0 and seatTopLeft == None:
          if seatGrid[topIdx][leftIdx] == ".":
            topIdx -= 1
            leftIdx -= 1
          else:
            seatTopLeft = seatGrid[topIdx][leftIdx]

        seatBottomLeft = None
        bottomIdx = rowIdx + 1
        leftIdx = colIdx - 1
        while bottomIdx < numRows and leftIdx >= 0 and seatBottomLeft == None:
          if seatGrid[bottomIdx][leftIdx] == ".":
            bottomIdx += 1
            leftIdx -= 1
          else:
            seatBottomLeft = seatGrid[bottomIdx][leftIdx]

        seatTopRight = None
        topIdx = rowIdx - 1
        rightIdx = colIdx + 1
        while topIdx >= 0 and rightIdx < numCols and seatTopRight == None:
          if seatGrid[topIdx][rightIdx] == ".":
            topIdx -= 1
            rightIdx += 1
          else:
            seatTopRight = seatGrid[topIdx][rightIdx]

        seatBottomRight = None
        bottomIdx = rowIdx + 1
        rightIdx = colIdx + 1
        while bottomIdx < numCols and rightIdx < numCols and seatBottomRight == None:
          if seatGrid[bottomIdx][rightIdx] == ".":
            bottomIdx += 1
            rightIdx += 1
          else:
            seatBottomRight = seatGrid[bottomIdx][rightIdx]

        occupiedAround = [seatTop, seatBottom, seatLeft, seatTopLeft, seatBottomLeft, seatRight, seatTopRight, seatBottomRight].count('#')

        if seat == "L" and occupiedAround == 0:
          newSeatGrid[rowIdx][colIdx] = "#"
          numberOfMoves += 1
        elif seat == "#" and occupiedAround >= 5:
          newSeatGrid[rowIdx][colIdx] = "L"
          numberOfMoves += 1

    seatGrid = newSeatGrid
    
  numOccupied = 0
  for rowIdx in range(numRows):
    for colIdx in range(numCols):
      if seatGrid[rowIdx][colIdx] == "#":
        numOccupied += 1
      
  print(f"Part 2 - Solution: {numOccupied}")

if __name__ == "__main__":
  dirname = os.path.dirname(__file__)
  filename = os.path.join(dirname, "input.txt")

  with open(filename, "r") as fileInput:
    fileLines = fileInput.readlines()
    lines = [line.strip() for line in fileLines]
    seatGrid = [list(line) for line in lines]

    part1(seatGrid)
    part2(seatGrid)
