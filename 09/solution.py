import os

def anyTwoElementsSum(preamble, target):
  for idx, a in enumerate(preamble):
    for b in preamble[idx + 1:]:
      if a + b == target:
        return True
  return False

def part1(numbers):
  PREAMBLE_WINDOW = 25

  start = 0
  while start + PREAMBLE_WINDOW < len(numbers):
    targetIdx = start + PREAMBLE_WINDOW
    preamble = numbers[start:targetIdx]
    target = numbers[targetIdx]

    if anyTwoElementsSum(preamble, target) == False:
      print(f"Part 1 - Solution: {target}")
      return targetIdx

    start += 1

def part2(numbers, targetIdx):
  target = numbers[targetIdx]

  # Find countiguous set of at least 2 numbers that add up to target
  for idx in range(len(numbers)):
    setSize = 2
    while idx + setSize <= len(numbers):
      subset = numbers[idx:idx+setSize]
      if sum(subset) == target:
        # Solution is the sum of the smallest and largest element in the subset
        print(f"Part 2 - Solution: {min(subset) + max(subset)}")
        return
      setSize += 1

if __name__ == "__main__":
  dirname = os.path.dirname(__file__)
  filename = os.path.join(dirname, "input.txt")

  with open(filename, "r") as fileInput:
    fileLines = fileInput.readlines()
    lines = [line.strip() for line in fileLines]
    numbers = [int(number) for number in lines]

    targetIdx = part1(numbers)
    part2(numbers, targetIdx)
