def part1(inputMap):
  rows = len(inputMap)
  cols = len(inputMap[0])

  rowIdx = 0
  colIdx = 0
  trees = 0
  while rowIdx < rows - 1:
    rowIdx += 1
    colIdx += 3

    # We went past the end of the column
    if colIdx >= cols:
      colIdx = colIdx - cols

    row = inputMap[rowIdx]
    spot = row[colIdx]

    if spot == "#":
      trees += 1

  print("Part 1 - Solution: " + str(trees))

def part2(inputMap):
  rows = len(inputMap)
  cols = len(inputMap[0])

  tests = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]

  treesProduct = 0
  for (rightSteps, downSteps) in tests: 
    rowIdx = 0
    colIdx = 0
    trees = 0
    while rowIdx < rows - 1:
      rowIdx += downSteps
      colIdx += rightSteps

      # We went past the end of the column
      if colIdx >= cols:
        colIdx = colIdx - cols

      row = inputMap[rowIdx]
      spot = row[colIdx]

      if spot == "#":
        trees += 1
    
    if (trees > 0):
      if treesProduct == 0:
        treesProduct = trees
      else:
        treesProduct *= trees

    print(f"Part 2 - Solution: {rightSteps} - {downSteps}: {trees}")

  print(f"Part 2 - Solution (Product): {treesProduct}")

if __name__ == "__main__":
  with open("input.txt", "r") as inputFile:
    fileLines = inputFile.readlines()
    inputMap = [ list(line.strip()) for line in fileLines]
    # print(inputMap[:3])

    part1(inputMap)
    part2(inputMap)