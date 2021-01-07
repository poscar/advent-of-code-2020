import os
import re
import math

# Part 1 is to find field values in nearbyTickets that do not match any rules
# and add them together
def part1(fieldRules, nearbyTickets):
  ruleRangeTuples = []
  for ruleValues in fieldRules.values():
    for rangeTuple in ruleValues:
      ruleRangeTuples.append(rangeTuple)

  invalidValues = []
  for nearbyTicket in nearbyTickets:
    for fieldValue in nearbyTicket:
      isValid = False
      for rangeTuple in ruleRangeTuples:
        minVal = rangeTuple[0]
        maxVal = rangeTuple[1]
        if fieldValue >= minVal and fieldValue <= maxVal:
          isValid = True
          break
      
      if not isValid:
        invalidValues.append(fieldValue)

  print(f"Part 1 - Solution: {sum(invalidValues)}")

# Discard the invalid tickets and use the rest of the nearbyTickets to figure
# out the fields, then look for the six fields on your ticket that start with
# the word departure. What do you get if you multiply those six values together?
def part2(fieldRules, nearbyTickets, yourTicket):
  ruleRangeTuples = []
  for ruleValues in fieldRules.values():
    for rangeTuple in ruleValues:
      ruleRangeTuples.append(rangeTuple)

  validNearbyTickets = []
  for nearbyTicket in nearbyTickets:
    validTicket = True
    for fieldValue in nearbyTicket:
      isValid = False
      for rangeTuple in ruleRangeTuples:
        minVal = rangeTuple[0]
        maxVal = rangeTuple[1]
        if fieldValue >= minVal and fieldValue <= maxVal:
          isValid = True
          break
      
      if not isValid:
        validTicket = False
        break
    if validTicket:
      validNearbyTickets.append(nearbyTicket)

  fieldIdxToValidRuleNames = {}
  for fieldIdx in range(len(fieldRules)):
    fieldIdxToValidRuleNames[fieldIdx] = set(fieldRules.keys())

  for ticket in validNearbyTickets:
    for fieldIdx, fieldValue in enumerate(ticket):
      for ruleName, ruleValues in fieldRules.items():
        isValid = False
        for rangeTuple in ruleValues:
          minVal = rangeTuple[0]
          maxVal = rangeTuple[1]
          if fieldValue >= minVal and fieldValue <= maxVal:
            isValid = True
            break

        # If isValid is false, ruleName has not been satisfied and we must removed from map
        if not isValid:
          fieldIdxToValidRuleNames[fieldIdx].remove(ruleName)

  
  pendingFieldNames = set(fieldRules.keys())
  fieldIdxToDeducedField = {}
  # print(f"possible fields: {pendingFieldNames}")
  # print(f"valid rules for fields: {fieldIdxToValidRuleNames}")
  while len(pendingFieldNames) > 0:
    newPendingFilenames = pendingFieldNames.copy()
    for fieldIdx, validRuleNames in fieldIdxToValidRuleNames.items():
      if len(validRuleNames) == 1:
        fieldName = validRuleNames.pop()
        fieldIdxToDeducedField[fieldIdx] = fieldName
        newPendingFilenames.remove(fieldName)
        for otherValidRuleNames in fieldIdxToValidRuleNames.values():
            otherValidRuleNames.discard(fieldName)

    if len(newPendingFilenames) == len(pendingFieldNames):
      print(f"could not deduce any fields...")
      break
    pendingFieldNames = newPendingFilenames

  # print(f"deduced fields: {fieldIdxToDeducedField}")
  deducedFieldToFieldIdx = {fieldName:fieldIdx for fieldIdx, fieldName in fieldIdxToDeducedField.items()}

  # Look for the six fields on your ticket that start with the word departure. What do you get if you multiply those six values together?
  departureValues = []
  for fieldName in fieldRules:
    if fieldName.startswith('departure'):
      departureValues.append(yourTicket[deducedFieldToFieldIdx[fieldName]])

  print(f"Part 2 - Solution {math.prod(departureValues)}")

TICKET_FIELD_RULE_REGEX = re.compile(r"([\w ]+): (\d+)-(\d+) or (\d+)-(\d+)")
if __name__ == "__main__":
  dirname = os.path.dirname(__file__)
  filename = os.path.join(dirname, "input.txt")

  with open(filename, "r") as fileInput:
    lines = [line.strip() for line in fileInput.readlines()]

    fieldRules = {}
    for line in lines:
      fieldRule = TICKET_FIELD_RULE_REGEX.match(line)
      if fieldRule != None:
        fieldRules[fieldRule[1]] = [(int(fieldRule[2]), int(fieldRule[3])), (int(fieldRule[4]), int(fieldRule[5]))]
      else:
        break
    
    yourTicket = [int(num) for num in lines[lines.index("your ticket:") + 1].split(",")]

    nearbyTicketsStartIdx = lines.index("nearby tickets:") + 1
    nearbyTickets = [[int(num) for num in line.split(",")] for line in lines[nearbyTicketsStartIdx:]]

    part1(fieldRules, nearbyTickets)
    part2(fieldRules, nearbyTickets, yourTicket)
