import os
import re
import time

def timeit(f):
  def wrapped(*args, **kwargs):
    start = time.perf_counter()
    result = f(*args, **kwargs)
    print(f"{f.__name__} took: {time.perf_counter() - start}s")
    return result
  return wrapped

def replaceRules(rule, rules):
  # Recursively replace reference to rules with their actual values
  if rule['type'] == "or" or rule['type'] == "and":
    ruleValue = rule['value']
    for subRuleIdx, subRule in enumerate(ruleValue):
      if isinstance(subRule, str):
        subRuleKey = subRule
        ruleValue[subRuleIdx] = rules[subRuleKey]
      elif subRule["type"] != "literal":
        replaceRules(subRule, rules)

# Validates / matches a message using the target rule directly
def validateWithRule(message, targetRule, charIdx):
  targetRuleType = targetRule["type"]
  targetRuleValue = targetRule["value"]
  isValid = False
  if targetRuleType == 'and':
    allValid = True
    currCharIdx = charIdx
    for subRule in targetRuleValue:
      newIsValid, newCharIdx = validateWithRule(message, subRule, currCharIdx)
      if newIsValid:
        currCharIdx = newCharIdx
      else:
        allValid = False
        break
    isValid = allValid
    if isValid:
      charIdx = currCharIdx
  elif targetRuleType == 'or':
    anyValid = False
    currCharIdx = charIdx
    for subRule in targetRuleValue:
      newIsValid, newCharIdx = validateWithRule(message, subRule, currCharIdx)
      if newIsValid:
        anyValid = True
        currCharIdx = newCharIdx
        break
    isValid = anyValid
    if isValid:
      charIdx = currCharIdx
  elif targetRuleType == 'literal':
    if charIdx < len(message) and message[charIdx] == targetRuleValue:
      isValid = True
      charIdx += len(targetRuleValue)
    else:
      isValid = False
  else:
    raise Exception(f"Invalid rule type {targetRuleType}")
  return isValid, charIdx

# Creates a regex corresponding to the target rule
def regexForTargetRule(targetRule):
  targetRuleType = targetRule["type"]
  targetRuleValue = targetRule["value"]
  targetRuleRegex = ""
  if targetRuleType == "and":
    targetRuleRegex += r"(?:"
    for subRule in targetRuleValue:
      targetRuleRegex += regexForTargetRule(subRule)
    targetRuleRegex += r")"
  elif targetRuleType == "or":
    targetRuleRegex += r"(?:"
    for idx, subRule in enumerate(targetRuleValue):
      targetRuleRegex += regexForTargetRule(subRule)
      if idx + 1 < len(targetRuleValue):
        targetRuleRegex += r"|"
    targetRuleRegex += r")"
  elif targetRuleType == 'literal':
    targetRuleRegex += targetRuleValue
  else:
    raise Exception('Invalid rule type')
  return targetRuleRegex

@timeit
def solveCustom(rules, messages):
  targetRule = rules['0']

  # Validate message with target rule with custom validator
  validMessagesCount = 0
  for message in messages:
    (validMessage, charIdx) = validateWithRule(message, targetRule, 0)
    isValid = validMessage and charIdx == len(message)
    if isValid:
      validMessagesCount += 1
  return validMessagesCount

@timeit
def solveRegex(rules, messages):
  targetRule = rules['0']

  # Validate message with target rule using regex mapping
  targetRuleRegex = r"^" + regexForTargetRule(targetRule) + r"$"
  targetRuleCompiledRegex = re.compile(targetRuleRegex)
  validMessagesCount = 0
  for message in messages:
    if targetRuleCompiledRegex.match(message) != None:
      validMessagesCount += 1
  return validMessagesCount

def solve(rules, messages):
  # Replace reference to rules in the input with the literals
  for rule in rules.values():
    replaceRules(rule, rules)

  validMessagesCount = solveCustom(rules, messages)
  print(f"Solution (custom) {validMessagesCount}")

  validMessagesCount = solveRegex(rules, messages)
  print(f"Solution (regex) {validMessagesCount}")

def parseInput(lines):
  RULE_REGEX = re.compile(r"(?P<ruleNumber>\d+): (?:(?P<subRules>[\d \|]+)|\"(?P<replacement>[ab])\")")
  MAX_RULE_RECURSION = 10

  rules = {}
  messages = []
  for line in lines:
    matches = RULE_REGEX.match(line)
    if matches != None:
      # Parse original rules/grammar into a tree we can understand and manipulate
      ruleNumber = matches["ruleNumber"]
      subRules = matches["subRules"]
      replacement = matches["replacement"]
      if subRules != None:
        splitSubRules = subRules.split("|")
        if len(splitSubRules) > 1:
          # The following commented line is all we had for part 1
          # rules[ruleNumber] = { "type": "or", "value": [{ "type": "and", "value": subRule.strip().split(" ")} for subRule in splitSubRules] }
          ruleObjects = []
          for subRule in splitSubRules:
            subRuleReplacements = subRule.strip().split(" ")
            subRuleHasCycle = any([replacementRule == ruleNumber for replacementRule in subRuleReplacements])
            if subRuleHasCycle:
              # To handle Part 2, we make rules for a maximum number of recursions
              cycleIdx = subRuleReplacements.index(ruleNumber) # index of the cycle rule number
              count = 0
              while count < MAX_RULE_RECURSION:
                repetitions = count + 1
                ruleObjects.append({ "type": "and", "value": (subRuleReplacements[0:cycleIdx] * repetitions) + (subRuleReplacements[cycleIdx+1:] * repetitions)})
                count += 1
            else:
              ruleObjects.append({ "type": "and", "value": subRuleReplacements })
          rules[ruleNumber] = { "type": "or", "value": ruleObjects }
        else:
          rules[ruleNumber] = { "type": "and", "value": splitSubRules[0].strip().split(" ") }
      elif replacement != None:
        rules[ruleNumber] = { "type": "literal", "value": replacement }
      else:
        raise Exception("Invalid rule.")
    elif len(line.strip()) > 0:
      # Collect messages to validate
      messages.append(line.strip())
  return rules, messages

if __name__ == "__main__":
  dirname = os.path.dirname(__file__)

  filenamePart1 = os.path.join(dirname, "input.txt")
  with open(filenamePart1, "r") as fileInput:
    print("-- Part 1 --")
    rules, messages = parseInput(fileInput.readlines())
    solve(rules, messages)

  filenamePart2 = os.path.join(dirname, "inputPart2.txt")
  with open(filenamePart2, "r") as fileInput:
    print("-- Part 2 --")
    rules, messages = parseInput(fileInput.readlines())
    solve(rules, messages)


