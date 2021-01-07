import os

# Parses the math expression into a list, assumes it is well formed.
def parse(expression):
  parsedExpression = []

  currOperand = ''
  subExpressionNestingLevel = 0
  subExpression = None
  for c in expression:
    if subExpression != None:
      if subExpressionNestingLevel == 0 and c == ')':
        parsedExpression.append(parse(subExpression))
        subExpression = None
      else:
        subExpression += c
        if c == '(':
          subExpressionNestingLevel += 1
        elif c == ')':
          subExpressionNestingLevel -= 1
    else:
      if c == '(':
        subExpression = ''
      elif c == '*' or c == '+':
        if currOperand != '':
          parsedExpression.append(int(currOperand))
          currOperand = ''
        parsedExpression.append(c)
      elif c >= '0' and c <= '9':
        currOperand += c

  # If we have a remaining operand, we must add it to the parsed expression
  if currOperand != '':
    parsedExpression.append(int(currOperand))
    currOperand = ''
  
  return parsedExpression

def calculate(parsedExpression):
  # Recursively calculate nested expressions, this will produce a flattened parsed expression
  parsedExpression = [calculate(element) if isinstance(element, list) else element for element in parsedExpression]

  total = 0
  idx = 0
  while idx < len(parsedExpression):
    element = parsedExpression[idx]
    if element == '*':
      total *= parsedExpression[idx + 1]
      idx += 1
    elif element == '+':
      total += parsedExpression[idx + 1]
      idx += 1
    else:
      total = element
    
    idx += 1

  return total

def evaluateExpression(expression):
  parsedExpression = parse(expression)
  return calculate(parsedExpression)

def part1(lines):
  assert evaluateExpression("2 * 3 + (4 * 5)") ==26
  assert evaluateExpression("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 437
  assert evaluateExpression("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2") == 13632
  results = [evaluateExpression(line) for line in lines]
  print(f"Part 1 - Solution: {sum(results)}")

def calculateAdditionFirst(parsedExpression):
  # Recursively calculate nested expressions, this will produce a flattened parsed expression
  parsedExpression = [calculateAdditionFirst(element) if isinstance(element, list) else element for element in parsedExpression]

  # Evaluate all of the additions first and store all multiplications
  parsedExpressionOnlyMult = []

  total = None
  idx = 0
  while idx < len(parsedExpression):
    element = parsedExpression[idx]
    if element == '*':
      parsedExpressionOnlyMult.append(total)
      parsedExpressionOnlyMult.append(element)
      total = None
    elif element == '+':
      total += parsedExpression[idx + 1]
      idx += 1
    else:
      total = element
    idx += 1
  if total != None:
    parsedExpressionOnlyMult.append(total)

  # Finally, do all multiplications
  total = None
  idx = 0
  while idx < len(parsedExpressionOnlyMult):
    element = parsedExpressionOnlyMult[idx]
    if element == '*':
      total *= parsedExpressionOnlyMult[idx + 1]
      idx += 1
    elif element == '+':
      raise Exception('Should never get here, we did all additions first...')
    else:
      total = element
    idx += 1

  return total

def evaluateExpressionAdditionFirst(expression):
  parsedExpression = parse(expression)
  return calculateAdditionFirst(parsedExpression)

def part2(lines):
  assert evaluateExpressionAdditionFirst("2 * 3 + (4 * 5)") == 46
  assert evaluateExpressionAdditionFirst("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 1445
  assert evaluateExpressionAdditionFirst("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2") == 23340
  results = [evaluateExpressionAdditionFirst(line) for line in lines]
  print(f"Part 2 - Solution: {sum(results)}")

if __name__ == "__main__":
  dirname = os.path.dirname(__file__)
  filename = os.path.join(dirname, "input.txt")

  with open(filename, "r") as fileInput:
    lines = [line.strip() for line in fileInput.readlines()]

    part1(lines)
    part2(lines)
