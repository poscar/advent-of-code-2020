import os

def calculateWinnerScore(playerOneDeck, playerTwoDeck):
  winnerDeck = None
  if len(playerOneDeck) == 0:
    # Player one has an empty deck, so player two is the winner.
    winnerDeck = playerTwoDeck
  elif len(playerTwoDeck) == 0:
    # Player two has an empty deck, so player one is the winner.
    winnerDeck = playerOneDeck
  else:
    raise Exception("Neither player one nor player two has an empty deck.")

  # Once the game ends, you can calculate the winning player's score. The bottom card in their deck is worth
  # the value of the card multiplied by 1, the second-from-the-bottom card is worth the value of the card 
  # multiplied by 2, and so on. With 10 cards, the top card is worth the value on the card multiplied by 10.
  totalScore = 0
  currCardValue = len(winnerDeck)
  for card in winnerDeck:
    totalScore += card * currCardValue
    currCardValue -= 1

  return totalScore

# Play the game as defined in the inst
def part1(playerOneDeck, playerTwoDeck):
  round = 1
  while len(playerOneDeck) != 0 and len(playerTwoDeck) != 0:
    playerOneCard = playerOneDeck.pop(0)
    playerTwoCard = playerTwoDeck.pop(0)
    if playerOneCard > playerTwoCard:
      playerOneDeck.append(playerOneCard)
      playerOneDeck.append(playerTwoCard)
    elif playerTwoCard > playerOneCard:
      playerTwoDeck.append(playerTwoCard)
      playerTwoDeck.append(playerOneCard)
    else:
      raise Exception(f"Found duplicate cards playerOne: {playerOneCard} playerTwo: {playerTwoCard}")
    round += 1
  
  totalScore = calculateWinnerScore(playerOneDeck, playerTwoDeck)
  print(f"Part 1 - Solution: {totalScore}")

def playPartTwoGame(playerOneDeck, playerTwoDeck):
  deckOnePlayed = set()
  deckTwoPlayed = set()
  rounds = 1
  while len(playerOneDeck) != 0 and len(playerTwoDeck) != 0:
    # Before either player deals a card, if there was a previous round in this game that had exactly the 
    # same cards in the same order in the same players' decks, the game instantly ends in a win for player1.
    # Previous rounds from other games are not considered.
    deckAlreadyPlayed = tuple(playerOneDeck) in deckOnePlayed or tuple(playerTwoDeck) in deckTwoPlayed
    if deckAlreadyPlayed:
      return playerOneDeck, []
    else:
      deckOnePlayed.add(tuple(playerOneDeck))
      deckTwoPlayed.add(tuple(playerTwoDeck))

    playerOneCard = playerOneDeck.pop(0)
    playerTwoCard = playerTwoDeck.pop(0)

    # If both players have at least as many cards remaining in their deck as the value of the card they just
    # drew, the winner of the round is determined by playing a new game of Recursive Combat (see below).
    playerOneWinSubGame = False
    playerTwoWinSubGame = False
    needToPlaySubgame = len(playerOneDeck) >= playerOneCard and len(playerTwoDeck) >= playerTwoCard
    if needToPlaySubgame:
      newPlayerOneDeck = playerOneDeck[0:playerOneCard]
      newPlayerTwoDeck = playerTwoDeck[0:playerTwoCard]
      subPlayerOneDeck, subPlayerTwoDeck = playPartTwoGame(newPlayerOneDeck, newPlayerTwoDeck)
      playerOneWinSubGame = len(subPlayerOneDeck) > 0
      playerTwoWinSubGame = len(subPlayerTwoDeck) > 0

    playerOneWinner = playerOneCard > playerTwoCard
    playerTwoWinner = playerTwoCard > playerOneCard

    if playerOneWinSubGame or (not playerTwoWinSubGame and playerOneWinner):
      playerOneDeck.append(playerOneCard)
      playerOneDeck.append(playerTwoCard)
    elif playerTwoWinSubGame or playerTwoWinner:
      playerTwoDeck.append(playerTwoCard)
      playerTwoDeck.append(playerOneCard)
    else:
      raise Exception(f"Could not find a winner in round. deckAlreadyPlayed: {deckAlreadyPlayed} playerOne: {playerOneCard} playerTwo: {playerTwoCard}")
    rounds += 1

  return playerOneDeck, playerTwoDeck

def part2(playerOneDeck, playerTwoDeck):
  finalPlayerOneDeck, finalPlayerTwoDeck = playPartTwoGame(playerOneDeck, playerTwoDeck)
  totalScore = calculateWinnerScore(finalPlayerOneDeck, finalPlayerTwoDeck)
  print(f"Part 2 - Solution: {totalScore}")

if __name__ == "__main__":
  dirname = os.path.dirname(__file__)
  filename = os.path.join(dirname, "input.txt")

  with open(filename, "r") as fileInput:
    lines = [line.strip() for line in fileInput.readlines()]

    playerOneDeck = []
    playerTwoDeck = []
    currPlayer = None
    for line in lines:
      if line == "Player 1:":
        currPlayer = playerOneDeck
        continue
      if line == "Player 2:":
        currPlayer = playerTwoDeck
        continue

      if len(line) > 0:
        currPlayer.append(int(line))

    part1(playerOneDeck[:], playerTwoDeck[:])
    part2(playerOneDeck[:], playerTwoDeck[:])
