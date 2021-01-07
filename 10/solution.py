import os

def part1(adapters):
  sortedAdapters = sorted(adapters)

  differences = {
    1: 0,
    2: 0,
    3: 1, # Initialize as 1 because device joltage is always 3 more than the largest adapter
  }
  for idx in range(len(sortedAdapters)):
    prevAdapter = sortedAdapters[idx - 1] if idx > 0 else 0
    currAdapter = sortedAdapters[idx]
    differences[currAdapter - prevAdapter] += 1

  print(f"Part 1 - Solution: {differences[1] * differences[3]}")

waysMem = {} # For memoization
def countWays(sortedAdapters):
  ways = 0
  currAdapter = sortedAdapters[0]
  for nextIdx in range(1, len(sortedAdapters)):
    nextAdapter = sortedAdapters[nextIdx]

    if nextAdapter - currAdapter <= 3:
      nextWays = None
      if nextAdapter in waysMem:
        nextWays = waysMem[nextAdapter]
      else:
        nextWays = countWays(sortedAdapters[nextIdx:])
        waysMem[nextAdapter] = nextWays

      ways += 1 * (nextWays if nextWays > 0 else 1)
    else:
      break

  # print(f"Ways: {ways} for adapter {sortedAdapters[0]}")
  return ways

def part2(adapters):
  sortedAdapters = sorted(adapters)
  
  # Add socket and device to make the full chain
  fullChain = sortedAdapters[:]
  fullChain.insert(0, 0)
  fullChain.insert(len(sortedAdapters), sortedAdapters[-1] + 3)
  # print(fullChain)

  ways = countWays(fullChain)
  print(f"Part 2 - Solution: {ways}")

if __name__ == "__main__":
  dirname = os.path.dirname(__file__)
  filename = os.path.join(dirname, "input.txt")

  with open(filename, "r") as fileInput:
    fileLines = fileInput.readlines()
    lines = [line.strip() for line in fileLines]

    adapters = [int(adapter) for adapter in lines]

    part1(adapters)
    part2(adapters)
