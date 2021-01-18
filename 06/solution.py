import os

def part1(groupYesAnswers):
  uniqueYesAnswersPerGroup = []

  for group in groupYesAnswers:
    uniqueYesAnswers = set()
    for yesAnswers in group:
      for c in yesAnswers:
        uniqueYesAnswers.add(c)

    uniqueYesAnswersPerGroup.append(len(uniqueYesAnswers))

  print(f"Part 1 - Solution: {sum(uniqueYesAnswersPerGroup)}")

def part2(groupYesAnswers):
  commonYesAnswersPerGroup = []

  for group in groupYesAnswers:
    groupSize = 0
    yesAnswersCount = dict()
    for yesAnswers in group:
      groupSize += 1
      for c in yesAnswers:
        if c in yesAnswersCount:
          yesAnswersCount[c] += 1
        else:
          yesAnswersCount[c] = 1

    commonYesAnswers = []
    for key in yesAnswersCount:
      if yesAnswersCount[key] == groupSize:
        commonYesAnswers.append(key)

    commonYesAnswersPerGroup.append(len(commonYesAnswers))

  print(f"Part 2 - Solution: {sum(commonYesAnswersPerGroup)}")

if __name__ == "__main__":
  dirname = os.path.dirname(__file__)
  filename = os.path.join(dirname, "input.txt")
  with open(filename, "r") as fileInput:
    fileLines = fileInput.readlines()
    groupYesAnswers = []

    yesAnswers = []
    for idx, line in enumerate(fileLines):
      if line != "\n":
        yesAnswers.append(line.strip())

      if line == "\n" or idx + 1 >= len(fileLines):
        groupYesAnswers.append(yesAnswers)
        yesAnswers = []

    part1(groupYesAnswers)
    part2(groupYesAnswers)



      