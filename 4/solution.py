import collections
import re

def part1(passports):
  expectedAttributes = frozenset(["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]) #, "cid"]

  validPassports = 0
  for passport in passports:
    passportData = passport.split(" ")
    passportKeys = frozenset(attribute.split(":")[0] for attribute in passportData)

    if expectedAttributes.issubset(passportKeys):
      validPassports += 1

  print(f"Part 1 - Solution {validPassports}")

def part2(passports):
  # byr (Birth Year) - four digits; at least 1920 and at most 2002.
  # iyr (Issue Year) - four digits; at least 2010 and at most 2020.
  # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
  # hgt (Height) - a number followed by either cm or in:
  # If cm, the number must be at least 150 and at most 193.
  # If in, the number must be at least 59 and at most 76.
  # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
  # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
  # pid (Passport ID) - a nine-digit number, including leading zeroes.
  # cid (Country ID) - ignored, missing or not.
  def validateBirthYear(year):
    yearInt = int(year)
    return len(year) == 4 and yearInt >= 1920 and yearInt <= 2002
  def validateIssueYear(year):
    yearInt = int(year)
    return len(year) == 4 and yearInt >= 2010 and yearInt <= 2020
  def validateExpirationYear(year):
    yearInt = int(year)
    return len(year) == 4 and yearInt >= 2020 and yearInt <= 2030
  def validateHeight(height):
    regex = re.compile(r"^(\d+)(cm|in)$")
    result = regex.match(height)
    if result != None:
      value = result[1]
      units = result[2]
      valueInt = int(value)
      if units == "cm" and valueInt >= 150 and valueInt <= 193:
        return True
      elif units == "in" and valueInt >= 59 and valueInt <= 76:
        return True
    return False
  def validateHairColor(color):
    regex = re.compile(r"^#[0-9a-f]{6}$")
    result = regex.match(color)
    return result != None
  def validateEyeColor(color):
    regex = re.compile(r"^(?:amb|blu|brn|gry|grn|hzl|oth)$")
    result = regex.match(color)
    return result != None
  def validatePassportId(id):
    regex = re.compile(r"^\d{9}$")
    result = regex.match(id)
    return result != None
  def validateCountryId(id):
    return True

  expectedAttributes = frozenset(["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]) #, "cid"]
  validators = {
    "byr": validateBirthYear,
    "iyr": validateIssueYear,
    "eyr": validateExpirationYear,
    "hgt": validateHeight,
    "hcl": validateHairColor,
    "ecl": validateEyeColor,
    "pid": validatePassportId,
    "cid": validateCountryId,
  }

  validPassports = 0
  for passport in passports:
    validPassportKeys = set()

    passportData = passport.split(" ")
    for attribute in passportData:
      key, value = attribute.split(":")
      isValid = validators[key](value)

      #print(f"key: {key} value: {value} isValid: {isValid}")

      if isValid:
        validPassportKeys.add(key)
      elif key in validPassportKeys:
        validPassportKeys.remove(key)
        break
      else:
        break

    if expectedAttributes.issubset(validPassportKeys):    
      validPassports += 1

  print(f"Part 2 - Solution {validPassports}")

if __name__ == "__main__":
    with open("input.txt", "r") as fileInput:
      fileLines = fileInput.readlines()
      passports = []

      passport = ""
      for idx, line in enumerate(fileLines):
        if line != "\n":
          passport = line.strip() if passport == "" else f"{passport} {line.strip()}"
        
        if line == "\n" or idx + 1 >= len(fileLines):
          passports.append(passport)
          passport = ""

      part1(passports)
      part2(passports)
