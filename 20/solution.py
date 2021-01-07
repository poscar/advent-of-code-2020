import os
import numpy as np

# Tiles are 10x10 squares
TILE_LENGTH = 10

# 2d array representing the seamonster
SEA_MONSTER = np.array([
  [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#", " "], 
  ["#", " ", " ", " ", " ", "#", "#", " ", " ", " ", " ", "#", "#", " ", " ", " ", " ", "#", "#", "#"], 
  [" ", "#", " ", " ", "#", " ", " ", "#", " ", " ", "#", " ", " ", "#", " ", " ", "#", " ", " ", " "],
])

# Possible values for flipX and flipY
FLIP_VALUES = [False, True]

class Tile:
  def __init__(self, number):
    self.number = number
    self.top = set()
    self.right = set()
    self.bottom = set()
    self.left = set()

class Transformation:
  def __init__(self, flipX, flipY, numRot):
    self.flipX = flipX
    self.flipY = flipY
    self.numRot = numRot

def areTilesAdjacent(tilePixels, otherTilePixels, getTargetArray, getComparisonArray):
  targetArray = getTargetArray(tilePixels)

  for flipX in FLIP_VALUES:
    for flipY in FLIP_VALUES:
      comparisonTile = np.copy(otherTilePixels)
      if flipX:
        comparisonTile = np.fliplr(comparisonTile)
      if flipY:
        comparisonTile = np.flipud(comparisonTile)

      # Rotate the tile 0, 90, 180, and 270 degrees
      numRot = 0
      while numRot < 4:
        rotatedTile = np.rot90(comparisonTile, numRot)

        # Check other tile to see if it fits...
        if (targetArray == getComparisonArray(rotatedTile)).all():
          return True, Transformation(flipX, flipY, numRot)

        numRot += 1

  return False, Transformation(False, False, 0)

def tileMatchesTop(tilePixels, otherTilePixels):
  return areTilesAdjacent(tilePixels, otherTilePixels, lambda tile: tile[0], lambda tile: tile[-1])

def tileMatchesRight(tilePixels, otherTilePixels):
  return areTilesAdjacent(tilePixels, otherTilePixels, lambda tile: tile[:, -1], lambda tile: tile[:, 0])

def tileMatchesBottom(tilePixels, otherTilePixels):
  return areTilesAdjacent(tilePixels, otherTilePixels, lambda tile: tile[-1], lambda tile: tile[0])

def tileMatchesLeft(tilePixels, otherTilePixels):
  return areTilesAdjacent(tilePixels, otherTilePixels, lambda tile: tile[:, 0], lambda tile: tile[:, -1])

def populateTileMatches(tileObjs):
  # Find the matching top, right, bottom, left tiles for each individual tile...
  tileIdx = 0
  while tileIdx < len(tileObjs):
    tileObj = tileObjs[tileIdx]
    otherTileIdx = 0
    while otherTileIdx < len(tileObjs):
      if tileIdx == otherTileIdx:
        otherTileIdx += 1
        continue

      otherTileObj = tileObjs[otherTileIdx]

      # check if other tile matches top
      (tileMatches, _) = tileMatchesTop(tiles[tileObj.number], tiles[otherTileObj.number])
      if tileMatches:
        tileObj.top.add(otherTileObj.number)

      # check if other tile matches right
      (tileMatches, _) = tileMatchesRight(tiles[tileObj.number], tiles[otherTileObj.number])
      if tileMatches:
        tileObj.right.add(otherTileObj.number)

      # check if other tile matches bottom
      (tileMatches, _) = tileMatchesBottom(tiles[tileObj.number], tiles[otherTileObj.number])
      if tileMatches:
        tileObj.bottom.add(otherTileObj.number)

      # check if other tile matches left
      (tileMatches, _) = tileMatchesLeft(tiles[tileObj.number], tiles[otherTileObj.number])
      if tileMatches:
        tileObj.left.add(otherTileObj.number)

      otherTileIdx += 1
    tileIdx += 1

def getCornerTiles(tileObjs):
  cornerTiles = []
  for tileObj in tileObjs:
    # Determine if this is a corner tile
    hasAdjacentTopRight = (len(tileObj.top) == 0 and len(tileObj.right) == 0)
    hasAdjacentBottomRight = (len(tileObj.right) == 0 and len(tileObj.bottom) == 0)
    hasAdjacentBottomLeft = (len(tileObj.bottom) == 0 and len(tileObj.left) == 0)
    hasAdjacentTopLeft = (len(tileObj.left) == 0 and len(tileObj.top) == 0)
    if hasAdjacentTopRight or hasAdjacentBottomRight or hasAdjacentBottomLeft or hasAdjacentTopLeft:
      cornerTiles.append(tileObj)
  return cornerTiles

def setPixelsOnImage(image, rowOffset, colOffset, tilePixels):
  for rowIdx, row in enumerate(tilePixels):
    for colIdx, pixel in enumerate(row):
      image[rowOffset + rowIdx, colOffset + colIdx] = pixel

def getMatchingTile(matchFunction, currentTilePixels, tiles, usedTilesNumbers):
  matches = []
  for candidateTileNumber in tiles:
    if candidateTileNumber in usedTilesNumbers:
      continue
    
    candidateTilePixels = tiles[candidateTileNumber]

    # Check if candidate tile can be placed as determined by the matchFunction (one of the tileMatches* functions defined above)
    isMatch, transformations = matchFunction(currentTilePixels, candidateTilePixels)

    if isMatch:
      if transformations.flipX:
        candidateTilePixels = np.fliplr(candidateTilePixels)
      if transformations.flipY:
        candidateTilePixels = np.flipud(candidateTilePixels)

      candidateTilePixels = np.rot90(candidateTilePixels, transformations.numRot)
      matches.append((candidateTileNumber, candidateTilePixels))

  if len(matches) == 0:
    raise Exception("No matching tiles found.")
  
  return matches[0]

def generateImageFromTopLeft(tiles, currentTileNumber, currentTilePixels):
  # Determine size of final image
  imageLength = int(np.ceil(np.sqrt(len(tiles))))
  imagePixelLength = imageLength * TILE_LENGTH
  image = np.empty((imagePixelLength, imagePixelLength), str)
  imageNoBordersPixelLength = imageLength * (TILE_LENGTH - 2)
  imageNoBorders = np.empty((imageNoBordersPixelLength, imageNoBordersPixelLength), str)

  # Track used tiles
  usedTilesNumbers = []

  rowOffset = 0
  rowOffsetNoBorders = 0
  while rowOffset < imagePixelLength:
    rowTilePixels = currentTilePixels
    colOffset = 0
    colOffsetNoBorders = 0
    while colOffset < imagePixelLength:
      setPixelsOnImage(image, rowOffset, colOffset, currentTilePixels)
      setPixelsOnImage(imageNoBorders, rowOffsetNoBorders, colOffsetNoBorders, currentTilePixels[1:-1, 1:-1])
      usedTilesNumbers.append(currentTileNumber)

      colOffset += TILE_LENGTH
      colOffsetNoBorders += (TILE_LENGTH - 2)
      if colOffset < imagePixelLength:
        currentTileNumber, currentTilePixels = getMatchingTile(tileMatchesRight, currentTilePixels, tiles, usedTilesNumbers)
      
    rowOffset += TILE_LENGTH
    rowOffsetNoBorders += (TILE_LENGTH - 2)
    if rowOffset < imagePixelLength:
      currentTileNumber, currentTilePixels = getMatchingTile(tileMatchesBottom, rowTilePixels, tiles, usedTilesNumbers)

  return image, imageNoBorders

def hasSeaMonster(imageSegment):
  for rowIdx, imageRow in enumerate(imageSegment):
    for colIdx, imagePixel in enumerate(imageRow):
      seaMonsterPixel = SEA_MONSTER[rowIdx, colIdx]
      if seaMonsterPixel == "#" and imagePixel != seaMonsterPixel:
        return False
  return True

def countSeaMonsters(image):
  count = 0
  imageRowIdx = 0
  while imageRowIdx <= image.shape[0] - SEA_MONSTER.shape[0]:
    imageColIdx = 0
    while imageColIdx <= image.shape[1] - SEA_MONSTER.shape[1]:
      if hasSeaMonster(image[imageRowIdx:imageRowIdx + SEA_MONSTER.shape[0], imageColIdx:imageColIdx + SEA_MONSTER.shape[1]]):
        count += 1
      imageColIdx += 1
    imageRowIdx += 1
  return count

def printImage(image, tileInterval):
  for rowIdx, row in enumerate(image):
    if rowIdx % tileInterval == 0:
      print("")

    outputLine = ""
    for colIdx, pixel in enumerate(row):
      if colIdx % tileInterval == 0:
        outputLine += " "
      if pixel == "":
        outputLine += " "
      else:
        outputLine += pixel
    print(outputLine)

def part1(tiles):
  tileObjs = [Tile(tileNumber) for tileNumber in tiles]
  populateTileMatches(tileObjs)
  cornerTiles = getCornerTiles(tileObjs)
  productOfCornerTiles = np.prod([cornerTile.number for cornerTile in cornerTiles])
  print(f"Part 1 - Solution: {productOfCornerTiles}")

def part2(tiles):
  tileNumberToObjs = {}
  for tileNumber in tiles:
    tileObj = Tile(tileNumber)
    tileNumberToObjs[tileNumber] = tileObj

  populateTileMatches(list(tileNumberToObjs.values()))
  cornerTiles = getCornerTiles(list(tileNumberToObjs.values()))

  # Get corner tiles
  topRightTiles = [cornerTile for cornerTile in cornerTiles if (len(cornerTile.top) == 0 and len(cornerTile.right) == 0)]
  bottomRightTiles = [cornerTile for cornerTile in cornerTiles if (len(cornerTile.bottom) == 0 and len(cornerTile.right) == 0)]
  bottomLeftTiles = [cornerTile for cornerTile in cornerTiles if (len(cornerTile.bottom) == 0 and len(cornerTile.left) == 0)]
  topLeftTiles = [cornerTile for cornerTile in cornerTiles if (len(cornerTile.top) == 0 and len(cornerTile.left) == 0)]

  currentTileNumber = None
  currentTilePixels = None
  if len(topLeftTiles) == 1:
    currentTileNumber = topLeftTiles[0].number
    currentTilePixels = tiles[currentTileNumber]
  elif len(topRightTiles) == 1:
    currentTileNumber = topRightTiles[0].number
    currentTilePixels = tiles[currentTileNumber]
    # Make top right into top left... (flip X)
    currentTilePixels = np.fliplr(currentTilePixels)
  elif len(bottomRightTiles) == 1:
    currentTileNumber = bottomRightTiles[0].number
    currentTilePixels = tiles[currentTileNumber]
    # Make bottom right into top left... (flip X and flip Y)
    currentTilePixels = np.fliplr(currentTilePixels)
    currentTilePixels = np.flipud(currentTilePixels)
  elif len(bottomLeftTiles) == 1:
    currentTileNumber = bottomLeftTiles[0].number
    currentTilePixels = tiles[currentTileNumber]
    # Make bottom left into top left... (flip Y)
    currentTilePixels = np.flipud(currentTilePixels)
  
  image, imageNoBorders = generateImageFromTopLeft(tiles, currentTileNumber, currentTilePixels)

  if image is None:
    raise Exception("Could not find a supported corner to generate the image")

  print("\n------------- IMAGE -------------")
  printImage(image, TILE_LENGTH)

  print("\n------------- NO BORDERS -------------")
  printImage(imageNoBorders, TILE_LENGTH - 2)
    
  # Attempt to find sea monsters for every transformation of imageNoBorders
  for flipX in FLIP_VALUES:
    for flipY in FLIP_VALUES:
      imageToLookUp = np.copy(imageNoBorders)
      if flipX:
        imageToLookUp = np.fliplr(imageToLookUp)
      if flipY:
        imageToLookUp = np.flipud(imageToLookUp)

      # Rotate the image 0, 90, 180, and 270 degrees
      numRot = 0
      while numRot < 4:
        rotatedImage = np.rot90(imageToLookUp, numRot)
        numSeaMonsters = countSeaMonsters(rotatedImage)
        # If we find any sea monsters, this is a solution and we'll return
        if numSeaMonsters > 0:
          nonSeaMonsterPoundPixels = np.sum(rotatedImage == "#") - np.sum(SEA_MONSTER == "#") * numSeaMonsters
          print(f"\nPart 2 - Solution: {nonSeaMonsterPoundPixels}")
          return
        numRot += 1
  

if __name__ == "__main__":
  dirname = os.path.dirname(__file__)
  filename = os.path.join(dirname, "input.txt")

  with open(filename, "r") as fileInput:
    lines = [line.strip() for line in fileInput.readlines()]

    tiles = {}
    currentTileNumber = None
    currentTile = np.empty((TILE_LENGTH, TILE_LENGTH), str)
    tileRow = 0
    for line in lines:
      if len(line) == 0:
        # If this is an empty line in the input, we have to save the current tile
        # we're processing (if any) and clear the state
        if currentTileNumber != None:
          # Save tile
          tiles[currentTileNumber] = currentTile
          # Clear state
          currentTileNumber = None
          currentTile = np.empty((TILE_LENGTH, TILE_LENGTH), str)
          tileRow = 0
      elif line.startswith("Tile"):
        # Store the tile number for processing
        currentTileNumber = int(line.split(" ")[1][:-1])
      else:
        # Parse tile
        for tileCol, pixel in enumerate(line):
          currentTile[tileRow, tileCol] = pixel
        tileRow += 1

    part1(tiles)
    part2(tiles)
