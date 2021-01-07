import os

def part1(directions):
  compass = ["N", "E", "S", "W"]
  currOrientation = "E"
  distances = {
    "N": 0,
    "S": 0,
    "E": 0,
    "W": 0
  }

  for direction in directions:
    instruction = direction[0]
    value = int(direction[1:])
    if instruction == "N" or instruction == "S" or instruction == "E" or instruction == "W":
      distances[instruction] += value
    elif instruction == "L" or instruction == "R":
      turns = int(value / 90)
      currIdx = compass.index(currOrientation)
      destIdx = (currIdx + (turns if instruction == "R" else -turns)) % len(compass)
      currOrientation = compass[destIdx]
    elif instruction == "F":
      distances[currOrientation] += value

  manhattanDistance = abs(distances["N"] - distances["S"]) + abs(distances["W"] - distances["E"])
  print(f"Part 1 - Solution {manhattanDistance}")

def part2(directions):
  compass = ["N", "E", "S", "W"]
  waypointLocation = {
    "N": 1,
    "S": 0,
    "E": 10,
    "W": 0
  }
  distances = {
    "N": 0,
    "S": 0,
    "E": 0,
    "W": 0
  }

  for direction in directions:
    instruction = direction[0]
    value = int(direction[1:])
    if instruction == "N" or instruction == "S" or instruction == "E" or instruction == "W":
      waypointLocation[instruction] += value
    elif instruction == "L" or instruction == "R":
      turns = int(value / 90)
      newWaypointLocation = {}
      for orientation in waypointLocation:
        currIdx = compass.index(orientation)
        destIdx = (currIdx + (turns if instruction == "R" else -turns)) % len(compass)
        newOrientation = compass[destIdx]
        newWaypointLocation[newOrientation] = waypointLocation[orientation]
      waypointLocation = newWaypointLocation
    elif instruction == "F":
      for orientation in waypointLocation:
        distances[orientation] += value * waypointLocation[orientation]

  manhattanDistance = abs(distances["N"] - distances["S"]) + abs(distances["W"] - distances["E"])
  print(f"Part 2 - Solution {manhattanDistance}")

if __name__ == "__main__":
  dirname = os.path.dirname(__file__)
  filename = os.path.join(dirname, "input.txt")

  with open(filename, "r") as fileInput:
    fileLines = fileInput.readlines()
    directions = [line.strip() for line in fileLines]

    part1(directions)
    part2(directions)
