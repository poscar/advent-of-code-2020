if __name__ == "__main__":
  with open("input.txt", "r") as inputFile:
    lines = inputFile.readlines()

    validPasswords = 0
    for line in lines:
      rule, password = line.split(": ")
      ruleRange, ruleChar = rule.split(" ")
      ruleRangeMin, ruleRangeMax = [int(n) for n in ruleRange.split("-")]
      charCount = 0
      for c in password:
        if c == ruleChar:
          charCount += 1

      if charCount >= ruleRangeMin and charCount <= ruleRangeMax:
        validPasswords += 1

    print("Part 1 - valid passwords:" + str(validPasswords))

    validPasswords = 0
    for line in lines:
      rule, password = line.split(": ")
      rulePosition, ruleChar = rule.split(" ")
      rulePositionOne, rulePositionTwo = [int(n) for n in rulePosition.split("-")]
      idxOne = rulePositionOne - 1
      idxTwo = rulePositionTwo - 1

      if (password[idxOne] == ruleChar and password[idxTwo] != ruleChar) or (password[idxOne] != ruleChar and password[idxTwo] == ruleChar):
        validPasswords += 1

    print("Part 2 - valid passwords:" + str(validPasswords))