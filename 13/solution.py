import os
import math

def part1(targetDeparture, availableBuses):
  nextDepartures = []
  for bus in availableBuses:
    closestDeparture = (targetDeparture // bus) * bus
    if closestDeparture >= targetDeparture:
      nextDepartures.append((bus, closestDeparture - targetDeparture))
    else:
      nextDepartures.append((bus, (closestDeparture + bus) - targetDeparture))
  nextDeparturesSorted = sorted(nextDepartures, key=lambda nextDeparture : nextDeparture[1])
  print(f"Part 1 - Solution: {nextDeparturesSorted[0][0]*nextDeparturesSorted[0][1]}")

def lcm(a, b):
  # a * b = LCM(a,b) * GCD(a,b)
  return a * b // math.gcd(a, b)

def part2(buses):
  validBuses = filter(lambda bus: bus != None, buses)
  busesMap = {}
  for idx, bus in enumerate(buses):
    if bus != None:
      busesMap[idx] = bus

  maxDeparture = math.prod(validBuses)
  validDeparture = 0
  stepSize = 1
  # Step through every bus finding a departure time that is valid for both the previous
  # valid departure and itself. Every time the step size is increased
  # by the largest common multiple of the current step size and the current bus.
  for busIdx in busesMap:
    currBus = busesMap[busIdx]
    for candidateDeparture in range(validDeparture, maxDeparture, stepSize):
      if (candidateDeparture + busIdx) % currBus == 0:
        validDeparture = candidateDeparture
        stepSize = lcm(stepSize, currBus)
        break

  print(f"Part 2 - Solution: {validDeparture}")

if __name__ == "__main__":
  dirname = os.path.dirname(__file__)
  filename = os.path.join(dirname, "input.txt")

  with open(filename, "r") as fileInput:
    fileLines = fileInput.readlines()
    lines = [line.strip() for line in fileLines]
    
    targetDeparture = int(lines[0])
    buses = [ int(bus) if bus != "x" else None for bus in lines[1].split(",")]
    availableBuses = filter(lambda bus: bus != None, buses)

    part1(targetDeparture, availableBuses)
    part2(buses)
