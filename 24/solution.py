import os

def isCompoundDirectionValid(compoundDirection):
  return compoundDirection in frozenset(["ne", "se", "sw", "nw"])

def getBlackTiles(directions):
  blackTiles = set()
  for tile in directions:
    x = 0
    y = 0

    dirIdx = 0
    while dirIdx < len(tile):
      compoundDirection = tile[dirIdx:dirIdx+2]
      simpleDirection = tile[dirIdx:dirIdx+1]

      if isCompoundDirectionValid(compoundDirection):
        if compoundDirection == "ne":
          x += 0.5
          y += 1
        elif compoundDirection == "se":
          x += 0.5
          y -= 1
        elif compoundDirection == "sw":
          x -= 0.5
          y -= 1
        elif compoundDirection == "nw":
          x -= 0.5
          y += 1
        dirIdx += 2        
      else:
        if simpleDirection == "e":
          x += 1
        elif simpleDirection == "w":
          x -= 1
        else:
          raise Exception(f"Invalid direction: {simpleDirection}")
        dirIdx += 1
      
    tileCoord = (x,y)
    if tileCoord in blackTiles:
      blackTiles.remove(tileCoord)
    else:
      blackTiles.add(tileCoord)

  return blackTiles

def getAdjacentBlacks(blackTiles, tile):
  (x, y) = tile
  adjacentBlacks = 0
  # Check tiles adjacent to this one
  if (x + 0.5, y + 1) in blackTiles:
    adjacentBlacks += 1
  if (x + 1, y) in blackTiles:
    adjacentBlacks += 1
  if (x + 0.5, y - 1) in blackTiles:
    adjacentBlacks += 1
  if (x - 0.5, y - 1) in blackTiles:
    adjacentBlacks += 1
  if (x - 1, y) in blackTiles:
    adjacentBlacks += 1
  if (x -0.5, y + 1) in blackTiles:
    adjacentBlacks += 1
  return adjacentBlacks

def part1(directions):
  blackTiles = getBlackTiles(directions)
  return len(blackTiles)

def part2(directions):
  DAYS = 100

  blackTiles = getBlackTiles(directions)

  day = 1
  while day <= DAYS:
    newBlackTiles = set()

    # Any black tile with zero or more than 2 black tiles immediately
    # adjacent to it is flipped to white.
    for tile in blackTiles:
      adjacentBlacks = getAdjacentBlacks(blackTiles, tile)
      if not (adjacentBlacks == 0 or adjacentBlacks > 2):
        newBlackTiles.add(tile)

    # Any white tile with exactly 2 black tiles immediately adjacent to it is flipped to black.
    processedPotentialWhiteTiles = set()
    for tile in blackTiles:
      (x, y) = tile
      targetTiles = [(x + 0.5, y + 1), (x + 1, y), (x + 0.5, y - 1), (x - 0.5, y - 1), (x - 1, y), (x -0.5, y + 1)]
      for targetTile in targetTiles:
        if targetTile not in processedPotentialWhiteTiles and targetTile not in blackTiles:
          # targetTile is a potential white tile, let's see if we should flip it black
          if getAdjacentBlacks(blackTiles, targetTile) == 2:
            newBlackTiles.add(targetTile)
        processedPotentialWhiteTiles.add(targetTile)

    blackTiles = newBlackTiles
    day += 1
  return len(blackTiles)

if __name__ == "__main__":
  dirname = os.path.dirname(__file__)

  testInputFilename = os.path.join(dirname, "testInput.txt")
  with open(testInputFilename, "r") as fileInput:
    inputLines = [line.strip() for line in fileInput.readlines()]
    assert part1(inputLines) == 10
    assert part2(inputLines) == 2208

  inputFilename = os.path.join(dirname, "input.txt")
  with open(inputFilename, "r") as fileInput:
    inputLines = [line.strip() for line in fileInput.readlines()]
    print(f"Part 1 - Solution: {part1(inputLines)}")
    print(f"Part 2 - Solution: {part2(inputLines)}")
