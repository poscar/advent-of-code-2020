import os

def performRound(currState, dims):
  BUFFER = [-1, 0, 1]
  newState = set()

  # Make a set containing all the coordinates to consider, meaning
  # those coordinates around the current state
  candidateCoordinates = set()
  for coordinate in currState:
    candidateCoordinates.add(coordinate)
    (x, y, z, w) = coordinate
    for wBuf in (BUFFER if dims == 4 else [0]):
      for zBuf in BUFFER:
        for yBuf in BUFFER:
          for xBuf in BUFFER:
            newCoordinate = (x + xBuf, y + yBuf, z + zBuf, w + wBuf)
            candidateCoordinates.add(newCoordinate)

  for coordinate in candidateCoordinates:
    (x, y, z, w) = coordinate
    activeCubesAround = 0
    for wBuf in BUFFER:
      for zBuf in BUFFER:
        for yBuf in BUFFER:
          for xBuf in BUFFER:
            testCoord = (x + xBuf, y + yBuf, z + zBuf, w + wBuf)
            if testCoord != coordinate and testCoord in currState:
              activeCubesAround += 1

    if (coordinate in currState and (activeCubesAround == 2 or activeCubesAround == 3)) or (coordinate not in currState and activeCubesAround == 3):
      newState.add(coordinate) 

  return newState

def solve(initialState, dims):
  ROUNDS = 6

  currState = initialState
  roundIdx = 0
  while roundIdx < ROUNDS:
    currState = performRound(currState, dims)
    roundIdx += 1

  return len(currState)

if __name__ == "__main__":
  dirname = os.path.dirname(__file__)
  filename = os.path.join(dirname, "input.txt")

  with open(filename, "r") as fileInput:
    lines = [line.strip() for line in fileInput.readlines()]

    # Initial state will only track the coordinates of the active states
    # Added an extra dimension for Part 2
    initialState = set()
    for y, line in enumerate(lines):
      for x, char in enumerate(line):
        if char == "#":
          initialState.add((x, y, 0, 0))

    # Solve function takes in the number of dimensions to consider while solving
    # as the second argument
    print(f"Part 1 - Solution {solve(initialState, 3)}")
    print(f"Part 2 - Solution {solve(initialState, 4)}")
