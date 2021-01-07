import os

INITIAL_SUBJECT_NUMBER = 7
MAGIC_VALUE = 20201227

def transformWithSubjectNumber(currentValue, subjectNumber):
  currentValue *= subjectNumber
  currentValue %= MAGIC_VALUE
  return currentValue

def getEncryptionKeyFromPublicKey(myLoopSize, otherPublicKey):
  loopSize = 1
  encryptionKey = 1
  while loopSize <= myLoopSize:
    encryptionKey = transformWithSubjectNumber(encryptionKey, otherPublicKey)
    loopSize += 1
  return encryptionKey

def getEncryptionKey(cardPublicKey, doorPublicKey):
  cardLoopSize = None
  doorLoopSize = None
  currentValue = 1
  loopSize = 1
  while cardLoopSize == None or doorLoopSize == None:
    currentValue = transformWithSubjectNumber(currentValue, INITIAL_SUBJECT_NUMBER)

    if cardLoopSize == None and cardPublicKey == currentValue:
      cardLoopSize = loopSize

    if doorLoopSize == None and doorPublicKey == currentValue:
      doorLoopSize = loopSize

    loopSize += 1

  print(f"cardLoopSize: {cardLoopSize} - doorLoopSize: {doorLoopSize}")

  # Generate encryption key using the smaller loopSize
  targetLoopSize = cardLoopSize if cardLoopSize <= doorLoopSize else doorLoopSize
  otherPublicKey = doorPublicKey if cardLoopSize <= doorLoopSize else cardPublicKey
  return getEncryptionKeyFromPublicKey(targetLoopSize, otherPublicKey)

def getPublicKeysFromInput(filename):
  with open(filename, "r") as fileInput:
    publicKeys = [int(line.strip()) for line in fileInput.readlines()]
    cardPublicKey = publicKeys[0]
    doorPublicKey = publicKeys[1]
    return cardPublicKey, doorPublicKey

if __name__ == "__main__":
  dirname = os.path.dirname(__file__)

  testFilename = os.path.join(dirname, "testInput.txt")
  cardPublicKey, doorPublicKey = getPublicKeysFromInput(testFilename)
  assert getEncryptionKey(cardPublicKey, doorPublicKey) == 14897079

  inputFilename = os.path.join(dirname, "input.txt")
  cardPublicKey, doorPublicKey = getPublicKeysFromInput(inputFilename)
  print(f"Part 1 - Solution: {getEncryptionKey(cardPublicKey, doorPublicKey)}")
