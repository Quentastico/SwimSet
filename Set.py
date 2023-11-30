## GLOBAL VARIABLES

import numpy as np
import globals
from utils import cutSetStaged

class Set:

  # Initialisation function
  def __init__(self, distance):

    # Attributes
    self.distance = distance # Distance of the set (m)
    self.distanceVariation = None # Type of variation of distances for the different blocks composing the Set
    self.listBlockDistance = [] # List of the distances of the block composing the set (in m)

    # Finding the distances of the Blocks
    self.setDistanceVariation()

  def setDistanceVariation(self):

    # 1. Setting the type of variation
    self.distanceVariation = variationTypes[np.random.randint(low=0, high=len(variationTypes))]

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

    for distance in np.arange(minBlockDistance, self.distance + stepBlockDistance, stepBlockDistance):
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
    optionBlocks = cutSetStaged(distance = self.distance, minBlocks = minBlocksIncrease)

    # Choosing a random way
    selectedOptionBlock = optionBlocks[np.random.randint(low=0, high=len(optionBlocks))]

    # Constracting the distances of the blocks withtin the set
    self.listBlockDistance = np.arange(selectedOptionBlock[1], selectedOptionBlock[1] + (selectedOptionBlock[0]) * selectedOptionBlock[2], selectedOptionBlock[2])

  # Note: ensure that the blocks are not increasing too much
  # Note: Maybe choose in priorty high numbers of blocks
  def decreasingBlocks(self):

    # Finding all the ways to cut the set
    optionBlocks = cutSetStaged(distance = self.distance, minBlocks = minBlocksDecrease)

    # Choosing a random way
    selectedOptionBlock = optionBlocks[np.random.randint(low=0, high=len(optionBlocks))]

    # Constracting the distances of the blocks withtin the set
    self.listBlockDistance = np.flip(np.arange(selectedOptionBlock[1], selectedOptionBlock[1] + (selectedOptionBlock[0]) * selectedOptionBlock[2], selectedOptionBlock[2]))

  # Note: ensure that the blocks are not increasing too much
  # Note: Maybe choose in priorty high numbers of blocks
  # Note: Remove the central one and merge it
  def pyramidBlocks(self):

    # Finding all the ways to cut half the set
    optionBlocks = cutSetStaged(distance = self.distance/2, minBlocks = minBlocksPyramid)

    # Choosing a random way
    selectedOptionBlock = optionBlocks[np.random.randint(low=0, high=len(optionBlocks))]

    # Constracting the distances of the blocks withtin the set
    increasePyramid = np.arange(selectedOptionBlock[1], selectedOptionBlock[1] + (selectedOptionBlock[0]) * selectedOptionBlock[2], selectedOptionBlock[2])
    decreasePyramid = np.flip(increasePyramid)
    self.listBlockDistance = np.concatenate([increasePyramid, decreasePyramid])

