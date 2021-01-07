import filecmp

if __name__ == "__main__":
    inputFile = open("input", "r")
    fileLines = inputFile.readlines()
    numbers = [int(line) for line in fileLines]

    found = False
    for i in range(len(numbers)):
      for j in range(i, len(numbers)):
        numbersI = numbers[i]
        numbersJ = numbers[j]
        if numbersI + numbersJ == 2020:
          found = True
          print("Part 1 Found: " + str(numbersI * numbersJ))
          break
      if found:
        break

    found = False
    for i in range(len(numbers)):
      for j in range(i, len(numbers)):
        for k in range(j, len(numbers)):
          numbersI = numbers[i]
          numbersJ = numbers[j]
          numbersK = numbers[k]
          if numbersI + numbersJ + numbersK == 2020:
            found = True
            print("Part 2 Found: " + str(numbersI * numbersJ * numbersK))
            break
        if found:
          break
      if found:
        break
      