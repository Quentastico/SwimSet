## GLOBAL VARIABLES

import numpy as np
import globals
from utils import splitSetPyramid
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
        optionBlocks = splitSetPyramid(distance = self.distance,
                                                stepBlockDistance = globals.stepBlockDistance,
                                                minBlockDistance = globals.minBlockDistance,
                                                minBlocks = globals.minBlocksIncrease)

        # Choosing a random way
        selectedOptionBlock = optionBlocks[np.random.randint(low=0, high=len(optionBlocks))]
        
        # Contracting the distances of the blocks withtin the set
        increasingBlockDistance = np.arange(selectedOptionBlock[1],
                                            selectedOptionBlock[1] + (selectedOptionBlock[0]+1) * selectedOptionBlock[2],
                                            selectedOptionBlock[2])
        decreasingBlockDistance = np.arange(selectedOptionBlock[1],
                                            selectedOptionBlock[1] + (selectedOptionBlock[0]) * selectedOptionBlock[2],
                                            selectedOptionBlock[2])

        self.listBlockDistance = np.concatenate([increasingBlockDistance, np.flip(decreasingBlockDistance)])
