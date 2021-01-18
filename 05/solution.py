import os
import math

def getRow(rowAssignment):
  low = 0
  high = 127
  for c in rowAssignment[:-1]:
    mid = low + (high - low) / 2

    if c == 'F':
      high = math.floor(mid)
    elif c == 'B':
      low = math.ceil(mid)

  lastC = rowAssignment[-1]
  if lastC == "F":
    return low
  elif lastC == 'B':
    return high


def getCol(colAssignment):
  low = 0
  high = 7
  for c in colAssignment[:-1]:
    mid = low + (high - low) / 2

    if c == 'L':
      high = math.floor(mid)
    elif c == 'R':
      low = math.ceil(mid)

  lastC = colAssignment[-1]
  if lastC == "L":
    return low
  elif lastC == 'R':
    return high

def part1(seats):
  seatIds = []
  for seat in seats:
    rowAssignment = seat[:7]
    colAssignment = seat[7:]
    row = getRow(rowAssignment)
    col = getCol(colAssignment)
    seatId = row * 8 + col
    seatIds.append(seatId)
    # print(f"row: {row} col: {col} id: {seatId}")
  
  print(f"Part 1 - Solution {max(seatIds)}")
  return seatIds



def part2(seatIds):
  missingSeatId = None
  sortedIds = sorted(seatIds)
  for idx, seatId in enumerate(sortedIds):
    seatIdAfter = None
    try:
      seatIdAfter = sortedIds[idx + 1]
    except:
      pass

    if seatId + 1 != seatIdAfter:
      missingSeatId = seatId + 1
      break

  print(f"Part 2 - Solution {missingSeatId}")


if __name__ == "__main__":
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "input.txt")
    with open(filename, "r") as inputFile:
      seats = [line.strip() for line in inputFile.readlines()]
      seatIds = part1(seats)
      part2(seatIds)