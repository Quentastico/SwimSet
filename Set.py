## GLOBAL VARIABLES

import numpy as np
import globals
from utils import cutSetStaged
from Block import Block
import utils

class Set:

  # Initialisation function
  def __init__(self, distance):

    # Attributes
    self.distance = distance # Distance of the set (m)
    self.distanceVariation = None # Type of variation of distances for the different blocks composing the Set
    self.listBlockDistance = [] # List of the distances of the block composing the set (in m)
    self.listBlocks = [] # List of the block objects that will compose the Set

    # Finding the distances of the Blocks
    self.setDistanceVariation()

    # Create the Blocks which are part of the Set
    self.createBlocks()

  def info(self):

    print("  SET - Distance: " + str(self.distance) + ", Variation of distance: " + str(self.distanceVariation) + ", List of Block distances: " + str(self.listBlockDistance))
    for block in self.listBlocks:
      block.info()

  def setDistanceVariation(self):

    # 1. Setting the type of variation
    self.distanceVariation = globals.variationTypes[np.random.randint(low=0, high=len(globals.variationTypes))]

    # 2. Calling the right method
    if self.distanceVariation == "equal":
      self.equalBlocks()

    if self.distanceVariation == "increasing":
      self.increasingBlocks()

    if self.distanceVariation == "decreasing":
      self.decreasingBlocks()

    if self.distanceVariation == "pyramid":
      self.pyramidBlocks()

  # Note: Maybe ensure that the blocks do not exceed a certain value
  def equalBlocks(self):

    # Calculating the possible number of blocks for a a given set

    optionDistanceBlock = []

    for distance in np.arange(globals.minBlockDistance, self.distance + globals.stepBlockDistance, globals.stepBlockDistance):
      if self.distance / distance == np.floor(self.distance / distance):
        optionDistanceBlock.append(distance)

    # Setting then randomly the distance
    blockDistance = optionDistanceBlock[np.random.randint(low=0, high=len(optionDistanceBlock))]

    # Finally setting the list of distance blocks
    for i in np.arange(int(self.distance / blockDistance)):
      self.listBlockDistance.append(blockDistance)

  # Note: ensure that the blocks are not increasing too much
  # Note: Maybe choose in priorty high numbers of blocks
  def increasingBlocks(self):

    # Finding all the ways to cut the set
    optionBlocks = cutSetStaged(distance = self.distance, minBlocks = globals.minBlocksIncrease)

    # Choosing a random way
    selectedOptionBlock = optionBlocks[np.random.randint(low=0, high=len(optionBlocks))]

    # Constracting the distances of the blocks withtin the set
    self.listBlockDistance = np.arange(selectedOptionBlock[1], selectedOptionBlock[1] + (selectedOptionBlock[0]) * selectedOptionBlock[2], selectedOptionBlock[2])

  # Note: ensure that the blocks are not increasing too much
  # Note: Maybe choose in priorty high numbers of blocks
  def decreasingBlocks(self):

    # Finding all the ways to cut the set
    optionBlocks = cutSetStaged(distance = self.distance, minBlocks = globals.minBlocksDecrease)

    # Choosing a random way
    selectedOptionBlock = optionBlocks[np.random.randint(low=0, high=len(optionBlocks))]

    # Constracting the distances of the blocks withtin the set
    self.listBlockDistance = np.flip(np.arange(selectedOptionBlock[1], selectedOptionBlock[1] + (selectedOptionBlock[0]) * selectedOptionBlock[2], selectedOptionBlock[2]))

  # Note: ensure that the blocks are not increasing too much
  # Note: Maybe choose in priorty high numbers of blocks
  # Note: Remove the central one and merge it
  def pyramidBlocks(self):

    # Finding all the ways to cut half the set
    optionBlocks = cutSetStaged(distance = self.distance/2, minBlocks = globals.minBlocksPyramid)

    # Choosing a random way
    selectedOptionBlock = optionBlocks[np.random.randint(low=0, high=len(optionBlocks))]

    # Constracting the distances of the blocks withtin the set
    increasePyramid = np.arange(selectedOptionBlock[1], selectedOptionBlock[1] + (selectedOptionBlock[0]) * selectedOptionBlock[2], selectedOptionBlock[2])
    decreasePyramid = np.flip(increasePyramid)
    self.listBlockDistance = np.concatenate([increasePyramid, decreasePyramid])

  # Function which defines the list of Blocks which compose the Set
  def createBlocks(self):

    # Case 1: All the blocks have the same distance ("constant") - then can allow blocks to have Segments
    if self.distanceVariation == "equal":

      # Here we will have to code something
      print("to be coded")

    else: 

      # We create a first block that contains exaclty one segment
      firstBlock = Block(distance=self.listBlockDistance[0], nSegments=1)

      # Then we decide if the intensity will increase, decrease or be constant from one block to the other
      relOptionIntensity = globals.optionIntensity[self.distanceVariation]
      selOptionIntensity = relOptionIntensity[np.random.randint(low=0, high=len(relOptionIntensity))]

      # Then we determine the intensities over the entire blocks
      listIntensities = utils.setIntensities(nBlocks=len(self.listBlockDistance), optionIntensity=selOptionIntensity, minIntensity=globals.minIntensity, maxIntensity=globals.maxIntensity, selectedIntensity=firstBlock.listSegment[0].intensity)

      # Finally we force the intensity of firstBlock to be equal to the first intensity and we add it to the list of blocks
      firstBlock.listSegment[0].intensity = listIntensities[0]
      self.listBlocks.append(firstBlock)

      firstBlock.listSegment[0].info()

      # Then we create the series of the other Blocks composing the segment
      if len(self.listBlockDistance) > 1:

        for i in np.arange(len(self.listBlockDistance)-1):

          # First we make a copy of the first Block created
          newBlock = firstBlock.copy()

          # We then change the distcnae of this new block
          newBlock.distance = self.listBlockDistance[i+1]

          # Then we only change the intensity & distance of this first block
          newBlock.listSegment[0].distance = self.listBlockDistance[i+1]
          newBlock.listSegment[0].intensity = listIntensities[i+1]

          # And finally we add each block to the list of blocks
          self.listBlocks.append(newBlock)

          












