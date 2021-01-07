import os
import re

def getAllIngredientsAndAllergens(foodItems):
  # Collect all ingredients and allergens by union of each foodItem's
  allIngredients = set()
  allAllergens = set()
  for foodItem in foodItems:
    allIngredients |= foodItem["ingredients"]
    allAllergens |= foodItem["allergens"]
  
  return allIngredients, allAllergens

def part1(foodItems):
  allIngredients, allAllergens = getAllIngredientsAndAllergens(foodItems)

  # Find all incredients that could countain an allergen
  ingredientsWithAllergens = set()
  for allergen in allAllergens:
    foodItemsWithAllergen = list(filter(lambda foodItem: allergen in foodItem["allergens"], foodItems))
    commonIngredients = set(foodItemsWithAllergen[0]["ingredients"])
    for foodItem in foodItemsWithAllergen[1:]:
      commonIngredients &= foodItem["ingredients"]
    ingredientsWithAllergens.update(commonIngredients)
  
  # Get all the ingredients that do not have any allergens
  cleanIngredients = allIngredients - ingredientsWithAllergens

  # Count how many times cleanIngredients appear in ingredient list
  totalCount = 0
  for ingredient in cleanIngredients:
    totalCount += sum([ingredient in foodItem["ingredients"] for foodItem in foodItems])

  print(f"Part 1 - Solution: {totalCount}")
  

def part2(lines):
  _, allAllergens = getAllIngredientsAndAllergens(foodItems)

  # Map each non-clean ingredient to the possible allergens it can contain
  ingredientToAllergens = {}
  for allergen in allAllergens:
    foodItemsWithAllergen = list(filter(lambda foodItem: allergen in foodItem["allergens"], foodItems))
    commonIngredients = set(foodItemsWithAllergen[0]["ingredients"])
    for foodItem in foodItemsWithAllergen[1:]:
      commonIngredients &= foodItem["ingredients"]

    for ingredient in commonIngredients:
      if ingredient not in ingredientToAllergens:
        ingredientToAllergens[ingredient] = set()
      ingredientToAllergens[ingredient].add(allergen)

  # Deduce the specific allergen each ingredient corresponds to
  allergenToIngredient = {}
  while len(allergenToIngredient) != len(ingredientToAllergens):
    for ingredient in ingredientToAllergens:
      allergens = ingredientToAllergens[ingredient]
      if len(allergens) == 1:
        allergen = allergens.pop()
        allergenToIngredient[allergen] = ingredient
        for ingredient in ingredientToAllergens:
          ingredientToAllergens[ingredient].discard(allergen)
        break

  # Sort the allergens alphabetically and get the corresponding ingredients
  nonCleanIngredientsSortedByAllergen = [allergenToIngredient[allergen] for allergen in sorted(allergenToIngredient.keys())]

  solution = ",".join(nonCleanIngredientsSortedByAllergen)
  print(f"Part 1 - Solution: {solution}")

if __name__ == "__main__":
  dirname = os.path.dirname(__file__)
  
  filename = os.path.join(dirname, "input.txt")
  with open(filename, "r") as fileInput:
    lines = [line.strip() for line in fileInput.readlines()]

    FOOD_REGEX = re.compile(r"^(?P<ingredients>(?:\w+ ?)+)(?: \(contains (?P<allergens>(?:\w+,? ?)+)\))?$")

    foodItems = []
    for food in lines:
      matches = FOOD_REGEX.match(food)
      ingredients = matches["ingredients"]
      allergens = matches["allergens"]
      if ingredients != None:
        ingredientsSet = set(ingredients.split(" "))
        allergensSet = set()
        if allergens != None:
          allergensSet = set(allergens.split(", "))
        foodItems.append({"ingredients": ingredientsSet, "allergens": allergensSet})

    part1(foodItems)
    part2(foodItems)
