import os
import re

def part1(bagRules):
  canContainShinyGold = set()
  target = "shiny gold"
  for bagColor in bagRules:
    rules = bagRules[bagColor]
    if target in rules and rules[target] > 0:
      canContainShinyGold.add(bagColor)

  additions = None
  while additions == None or additions > 0:
    additions = 0
    for bagColor in bagRules:
      rules = bagRules[bagColor]
      # If the rules indicate this color can contain any that can contain shiny gold
      rulesColors = set(rules.keys())
      if bagColor not in canContainShinyGold and len(rulesColors.intersection(canContainShinyGold)) > 0:
        additions += 1
        canContainShinyGold.add(bagColor)
  
  print(f"Part 1 - Solution: {len(canContainShinyGold)}")

def getBagsCount(bagRules, bagColor):
  rules = bagRules[bagColor]

  totalBagsCount = 0
  for ruleBagColor in rules:
    count = rules[ruleBagColor]
    childCount = getBagsCount(bagRules, ruleBagColor)
    totalBagsCount += count + count * childCount

  return totalBagsCount


def part2(bagRules):
  totalBags = getBagsCount(bagRules, "shiny gold")
  print(f"Part 2 - Solution: {totalBags}")

RULE_REGEX = re.compile(r"(?:(\d+) ([\w ]+) bags?)")
if __name__ == "__main__":
  dirname = os.path.dirname(__file__)
  filename = os.path.join(dirname, "input.txt")

  with open(filename, "r") as fileInput:
    fileLines = fileInput.readlines()

    bagRules = {}
    for line in fileLines:
      cleanLine = line.strip()
      bagColor, rules = cleanLine.split(" bags contain ")
      rulesSplit = rules.split(", ")

      ruleColorToCount = {}
      for rule in rulesSplit:
        if rule == "no other bags.":
          break
        
        parsedRule = RULE_REGEX.match(rule)
        if parsedRule != None:
          ruleCount = parsedRule[1]
          ruleBagColor = parsedRule[2]
          ruleColorToCount[ruleBagColor] = int(ruleCount)

      bagRules[bagColor] = ruleColorToCount

    part1(bagRules)
    part2(bagRules)



      