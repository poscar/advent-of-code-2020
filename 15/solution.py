import os
import time

def timeit(f):
  def wrapped(*args, **kwargs):
    start = time.perf_counter()
    result = f(*args, **kwargs)
    print(f"{f.__name__} took: {time.perf_counter() - start}s")
    return result
  return wrapped

def part1(numbers, targetTurn = 2020):
  counts = {}
  lastSeenIndices = {}

  # Initialize
  for turnIdx, number in enumerate(numbers):
    if number not in counts: counts[number] = 1
    else: counts[number] += 1
    if number not in lastSeenIndices: lastSeenIndices[number] = [turnIdx]
    else: lastSeenIndices[number].append(turnIdx)

  turnIdx = len(numbers)
  while turnIdx < targetTurn:
    lastSpoken = numbers[turnIdx - 1]

    numberSpoken = None
    if lastSpoken in counts and counts[lastSpoken] == 1:
      numberSpoken = 0
    else:
      numberSpokenLastIndices = lastSeenIndices[lastSpoken]
      numberSpoken = numberSpokenLastIndices[-1] - numberSpokenLastIndices[-2]

    if numberSpoken not in counts: counts[numberSpoken] = 1
    else: counts[numberSpoken] += 1
    if numberSpoken not in lastSeenIndices: lastSeenIndices[numberSpoken] = [turnIdx]
    else: lastSeenIndices[numberSpoken].append(turnIdx)

    numbers.append(numberSpoken)
    turnIdx += 1
  
  print(f"Target turn {targetTurn} - Solution {numbers[-1]}")

@timeit
def part2(numbers):
  part1(numbers, 30000000)

if __name__ == "__main__":
  dirname = os.path.dirname(__file__)
  filename = os.path.join(dirname, "input.txt")

  with open(filename, "r") as fileInput:
    lines = [line.strip() for line in fileInput.readlines()]
    for line in lines:
      numbers = [int(num) for num in line.split(",")]

      print(f"Input numbers: {numbers}")
      part1(numbers)
      part2(numbers)
