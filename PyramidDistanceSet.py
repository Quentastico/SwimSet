## GLOBAL VARIABLES

import numpy as np
import globals
from utils import splitSetPyramid
from IncreasingDecreasingDistanceSet import IncreasingDecreasingDistanceSet
from Block import Block
from Set import Set
import utils

class PyramidDistanceSet(Set):

    # Object initialisation
    def __init__(self, distance, standardInit = False):

        super().__init__(distance, standardInit = standardInit)

        self.type = "Pyramid Distance"
        self.increasingBlockDistance = [] # This list will contain the list of the distances withtin the distance block
        self.increasingSet = None # This will contain the IncreasingDecreasingSet of the first half of the pyramid

        if self.standardInit:
            self.setBlockDistances()
            self.createBlocks()

    # Method to split the set into a given distance
    def setBlockDistances(self): 

        # Finding all the ways to cut the set
        optionBlocks = splitSetPyramid(distance = self.distance, 
                                       stepBlockDistance = globals.stepBlockDistance,
                                       minBlockDistance = globals.minBlockDistance,
                                       minBlocks = globals.minBlocksPyramid)

        # Choosing a random way
        selectedOptionBlock = optionBlocks[np.random.randint(low=0, high=len(optionBlocks))]
        
        # Contracting the distances of the blocks withtin the set
        increasingBlockDistance = np.arange(selectedOptionBlock[1],
                                            selectedOptionBlock[1] + (selectedOptionBlock[0]+1) * selectedOptionBlock[2],
                                            selectedOptionBlock[2])
        self.increasingBlockDistance = increasingBlockDistance
        decreasingBlockDistance = np.arange(selectedOptionBlock[1],
                                            selectedOptionBlock[1] + (selectedOptionBlock[0]) * selectedOptionBlock[2],
                                            selectedOptionBlock[2])

        self.listBlockDistance = np.concatenate([increasingBlockDistance, np.flip(decreasingBlockDistance)])

    # Method to create the blocks
    # The method here is pretty simple: we create an increasing block distance and we mirror the blocks
    def createBlocks(self):

        # STEP 1: We need to create an Increasing Set

        # We first create an Increasing/Decreasing Set based on the increasing block distance
        # Note: Here it is important to ensure that standardInit = False to avoid recreating the distance. 
        increasingSet = IncreasingDecreasingDistanceSet(distance=np.sum(self.increasingBlockDistance), standardInit=False)

        # We then need to force the block distance list &  the type (increase)
        increasingSet.listBlockDistance = self.increasingBlockDistance
        increasingSet.increaseDecrease = "increase"

        # The sequence type can then be determined "normally"
        increasingSet.setSequenceType()

        # Finally the blocks of the set can be created by using the normal function
        increasingSet.createBlocks()

        # TO REMOVE
        self.increasingSet = increasingSet

        # STEP 2: We then populate each Attribute of the pyramid set class

        # listBlocks & listBlockDistance
        listBlockDistance = increasingSet.listBlockDistance.copy()
        print(type(listBlockDistance))
        listBlock = increasingSet.listBlock.copy()
        print(type(listBlock))
        nBlocks = len(listBlock)
        for i in np.arange(nBlocks):
            listBlockDistance.append(listBlockDistance[nBlocks-2-i])
            listBlock.append(listBlock[nBlocks-2-i])
        self.listBlockDistance = listBlockDistance
        self.listBlock = listBlock

        # Variation Segment: Not populated

        # sequence Type
        self.sequenceType = increasingSet.sequenceType







