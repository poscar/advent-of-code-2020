import os
import re

MASK_REGEX = re.compile(r"mask = (\S+)")
MEMORY_REGEX = re.compile(r"mem\[(\d+)\] = (\d+)")

def getMaskedValue(mask, value):
  output = [maskBit if maskBit != None else valueBit for (maskBit, valueBit) in zip(mask, value)]
  return output
  
def part1(lines):
    currentMask = []
    memory = {}
    for line in lines:
      parsedMask = MASK_REGEX.match(line)
      if parsedMask != None:
        currentMask = [c if c == "0" or c == "1" else None for c in parsedMask[1]]
      else:
        parsedMemory = MEMORY_REGEX.match(line)
        address = int(parsedMemory[1])
        value = int(parsedMemory[2])
        binValueStr = bin(value)[2:] # get bits after 0b part (0b1100 -> 1100)
        binValue = ["0"]*(len(currentMask) - len(binValueStr)) + [str(bit) for bit in binValueStr]
        memory[address] =  int("".join(getMaskedValue(currentMask, binValue)), 2)

    # print(memory)
    print(f"Part 1 - Solution: {sum(memory.values())}")

def getMaskedAddresses(mask, address):
  maskedAddress = [valueBit if maskBit == "0" else maskBit for (maskBit, valueBit) in zip(mask, address)]

  outAddresses = [maskedAddress]
  for idx, maskBit in enumerate(maskedAddress):
    # If maskBit is None, value could be Could be 0 or 1
    if maskBit == None:
      newAddresses = []
      for outAddress in outAddresses:
        outAddress[idx] = "0"
        newAddress = outAddress[:]
        newAddress[idx] = "1"
        newAddresses.append(newAddress)
      outAddresses += newAddresses
  
  return outAddresses

def part2(lines):
  currentMask = []
  memory = {}
  for line in lines:
    parsedMask = MASK_REGEX.match(line)
    if parsedMask != None:
      currentMask = [c if c == "0" or c == "1" else None for c in parsedMask[1]]
    else:
      parsedMemory = MEMORY_REGEX.match(line)
      address = int(parsedMemory[1])
      value = int(parsedMemory[2])
      binAddressStr = bin(address)[2:] # get bits after 0b part (0b1100 -> 1100)
      binAddress = ["0"]*(len(currentMask) - len(binAddressStr)) + [str(bit) for bit in binAddressStr]
      maskedAddresses = getMaskedAddresses(currentMask, binAddress)
      for maskedAddress in maskedAddresses:
        unmaskedAddress = int("".join(maskedAddress), 2)
        memory[unmaskedAddress] =  value

  # print(memory)
  print(f"Part 2 - Solution: {sum(memory.values())}")

if __name__ == "__main__":
  dirname = os.path.dirname(__file__)
  filename = os.path.join(dirname, "input.txt")

  with open(filename, "r") as fileInput:
    lines = [line.strip() for line in fileInput.readlines()]

    part1(lines)
    part2(lines)
