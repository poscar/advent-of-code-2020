import os
from LinkedList import Node, LinkedList
from Instrumentation import timeit

@timeit
def playCupsGame(cupsList, moves):
  maxCupValue = max(cupsList)
  minCupValue = min(cupsList)

  move = 1
  currCupIdx = 0
  while move <= moves:
    pickUpStartIdx = currCupIdx + 1
    pickUpEndIdx = pickUpStartIdx + 3
    pickedUpCups = cupsList[pickUpStartIdx:pickUpEndIdx]
    remainingCups = cupsList[currCupIdx:pickUpStartIdx] + cupsList[pickUpEndIdx:]

    # print(f"move {move}")
    # print(f"picked up cups {pickedUpCups}")
    # print(f"remaining cups {remainingCups}")

    currCupValue = cupsList[currCupIdx]
    destCupValue = (currCupValue - 1) if (currCupValue - 1) >= minCupValue else maxCupValue
    while destCupValue in pickedUpCups:
      destCupValue = (destCupValue - 1) if (destCupValue - 1) >= minCupValue else maxCupValue

    # print(f"destination cup {destCupValue}")
    destIdx = remainingCups.index(destCupValue) + 1

    # Make the next iteration starting cup list in the right order (0th element being the next current cup, last current cup at the end)
    nextCupsList = remainingCups[:destIdx] + pickedUpCups + remainingCups[destIdx:]
    nextCupsList.append(nextCupsList.pop(0))
    cupsList = nextCupsList
    move += 1
  
  return cupsList

@timeit
def playCupsGameFast(cupsList, moves):
  cupsList = LinkedList(cupsList)
  maxCupNode = max(cupsList)
  minCupNode = min(cupsList)

  move = 1
  while move <= moves:
    # print(f"move {move}")

    currCupNode = cupsList.head
    # print(f"current cups: {cupsList} with currCupValue: {currCupNode.data}")

    # Pick up cups
    pickedUpCupNodes = []
    pickedUpCups = []
    numPickedUp = 0
    cupToPickUp = currCupNode.next
    while numPickedUp < 3:
      pickedUpCups.append(cupToPickUp.data)
      pickedUpCupNodes.append(cupToPickUp)
      cupToPickUp = cupToPickUp.next
      numPickedUp += 1

    # print(f"picked up cups {pickedUpCups}")

    destCupValue = (currCupNode.data - 1) if (currCupNode.data - 1) >= minCupNode.data else maxCupNode.data
    while destCupValue in pickedUpCups:
      destCupValue = (destCupValue - 1) if (destCupValue - 1) >= minCupNode.data else maxCupNode.data

    # print(f"destination cup {destCupValue}")

    # Insert the picked up elements at their expected location
    currDestNode = cupsList.getNodeWithData(destCupValue)
    destNodeNext = currDestNode.next
    for pickedUpCup in pickedUpCupNodes:
      currDestNode.next = pickedUpCup
      currDestNode = pickedUpCup
    
    currCupNode.next = currDestNode.next
    currDestNode.next = destNodeNext
    
    cupsList.head = currCupNode.next
    move += 1
  
  return cupsList

def part1Slow(cups, moves):
  # Make a list out of the cups input
  cupsList = list([int(cup) for cup in cups])

  cupsList = playCupsGame(cupsList, moves)
  indexOfCupOne = cupsList.index(1)

  solutionCupsList = []
  for idx in range(indexOfCupOne + 1, len(cupsList)):
    solutionCupsList.append(cupsList[idx])
  for idx in range(0, indexOfCupOne):
    solutionCupsList.append(cupsList[idx])

  solutionCups = "".join([str(cup) for cup in solutionCupsList])
  return solutionCups

def part1Fast(cups, moves):
  # Make a list out of the cups input
  cupsList = list([int(cup) for cup in cups])

  cupsList = playCupsGameFast(cupsList, moves)
  cupOneNode = cupsList.getNodeWithData(1)

  solutionCupsList = []
  solutionCupNode = cupOneNode.next
  while solutionCupNode != cupOneNode:
    solutionCupsList.append(solutionCupNode)
    solutionCupNode = solutionCupNode.next

  solutionCups = "".join([str(cup) for cup in solutionCupsList])
  # print(solutionCups)
  return solutionCups

def part2(cups, moves):
  # Make a list out of the cups input
  cupsList = list([int(cup) for cup in cups])

  # Your labeling is still correct for the first few cups; after that, the remaining cups are just
  # numbered in an increasing fashion starting from the number after the highest number in your list
  # and proceeding one by one until one million is reached.
  FINAL_MAX_CUP_VALUE = 1000000
  cupsList += list(range(max(cupsList) + 1, FINAL_MAX_CUP_VALUE + 1))

  cupsList = playCupsGameFast(cupsList, moves)
  cupOneNode = cupsList.getNodeWithData(1)
  solutionValue = cupOneNode.next.data * cupOneNode.next.next.data
  return solutionValue

if __name__ == "__main__":
  sampleInput = "389125467"
  puzzleInput = "459672813"

  assert part1Fast(sampleInput, 10) == "92658374"
  assert part1Fast(sampleInput, 100) == "67384529"
  print(f"Part 1 - Solution: {part1Fast(puzzleInput, 100)}")

  assert part2(sampleInput, 10000000) == 149245887792
  print(f"Part 2 - Solution: {part2(puzzleInput, 10000000)}")
