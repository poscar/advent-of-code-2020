import os

def part1(instructions):
  acc = 0
  idx = 0
  visitedInstructions = set()
  while idx < len(instructions):
    visitedInstructions.add(idx)

    instruction = instructions[idx]
    operator, operand = instruction.split(" ")

    value = int(operand[1:])

    if operator == "acc":
      if operand[0] == "+":
        acc += value
      elif operand[0] == "-":
        acc -= value
      idx += 1
    elif operator == "jmp":
      if operand[0] == "+":
        idx += value
      elif operand[0] == "-":
        idx -= value
    elif operator == "nop":
      idx += 1

    # if the next instruction we will execute has already been executed, we break...
    if idx in visitedInstructions:
      break

  print(f"Part 1 - Solution: {acc}")

def verifyProgramTerminates(instructions):
  acc = 0
  idx = 0
  visitedInstructions = set()
  while idx < len(instructions):
    visitedInstructions.add(idx)

    instruction = instructions[idx]
    operator, operand = instruction.split(" ")

    value = int(operand)

    if operator == "acc":
      acc += value
      newIdx = idx + 1
    elif operator == "jmp":
      newIdx = idx + value
    elif operator == "nop":
      newIdx = idx + 1

    # if the next instruction we will execute has already been executed, we can try to fix it
    if newIdx in visitedInstructions:
      return (False, acc)
    else:
      idx = newIdx

  return (True, acc)

def part2(instructions):
  for idx, instruction in enumerate(instructions):
    operator, operand = instruction.split(" ")
    value = int(operand)

    fixedInstructions = instructions[:]
    if operator == "jmp":
      fixedInstructions[idx] = f"nop {value}"
    elif operator == "nop":
      fixedInstructions[idx] = f"jmp {value}"

    terminates, acc = verifyProgramTerminates(fixedInstructions)
    if terminates == True:
      print(f"Part 2 - Solution: {acc}")
      break

if __name__ == "__main__":
  dirname = os.path.dirname(__file__)
  filename = os.path.join(dirname, "input.txt")

  with open(filename, "r") as fileInput:
    fileLines = fileInput.readlines()
    instructions = [line.strip() for line in fileLines]

    part1(instructions)
    part2(instructions)
