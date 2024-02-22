## GLOBAL VARIABLES

import numpy as np
import globals
from utils import splitSetIncreaseDecrease
from Block import Block
from Set import Set
import utils

class IncreasingDistanceSet(Set):

    # Object initialisation
    def __init__(self, distance):
        super().__init__(distance)

    # Method to split the set into a given distance
    def setBlockDistances(self): 

        # Finding all the ways to cut the set
        optionBlocks = splitSetIncreaseDecrease(distance = self.distance, minBlocks = globals.minBlocksIncrease)

        # Choosing a random way
        selectedOptionBlock = optionBlocks[np.random.randint(low=0, high=len(optionBlocks))]
        
        # Constracting the distances of the blocks withtin the set
        self.listBlockDistance = np.arange(selectedOptionBlock[1], selectedOptionBlock[1] + (selectedOptionBlock[0]) * selectedOptionBlock[2], selectedOptionBlock[2])
