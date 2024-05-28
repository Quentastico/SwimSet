## IMPORTS

import numpy as np
from utils import splitSetPyramid
from IncreasingDecreasingDistanceSet import IncreasingDecreasingDistanceSet
from Block import Block
from Set import Set
import utils
import settings

class PyramidDistanceSet(Set):

    # Object initialisation
    def __init__(self, distance, standardInit=False, neutralSegment=None, focusSegment=None):

        super().__init__(distance, standardInit=standardInit, neutralSegment=neutralSegment, focusSegment=focusSegment)

        self.type = "Pyramid Distance"
        self.increasingBlockDistance = [] # This list will contain the list of the distances withtin the distance block
        self.increasingSet = None # This will contain the IncreasingDecreasingSet of the first half of the pyramid

        if self.standardInit:
            self.setBlockDistances()
            self.createBlocks()
            self.finalise()

    # Method to split the set into a given distance
    def setBlockDistances(self): 

        # Finding all the ways to cut the set
        optionBlocks = splitSetPyramid(distance = self.distance, 
                                       stepBlockDistance = settings.globals.stepBlockDistance,
                                       minBlockDistance = settings.globals.minBlockDistance,
                                       minBlocks = settings.globals.minBlocksPyramid)

        # Choosing an option
        # Note: the rule is that we pick a combination which number of blocks is as high as possible

        # 1. We need to determine what the maximum number of block is
        maxBlocks = 0
        for option in optionBlocks:
            if option[0] > maxBlocks:
                maxBlocks = option[0]
        print(maxBlocks)

        # 2. Then we extract from optionBlocks the options with the maximal number of blocks
        maxOptionBlocks = []
        for option in optionBlocks:
            if option[0] == maxBlocks:
                maxOptionBlocks.append(option)
        print(maxOptionBlocks)

        # 3. Finally we select the block within the selected options        
        selectedOptionBlock = maxOptionBlocks[np.random.randint(low=0, high=len(maxOptionBlocks))]
        
        # Contracting the distances of the blocks withtin the set
        increasingBlockDistance = list(np.arange(selectedOptionBlock[1],
                                            selectedOptionBlock[1] + (selectedOptionBlock[0]+1) * selectedOptionBlock[2],
                                            selectedOptionBlock[2]))
        self.increasingBlockDistance = increasingBlockDistance
        decreasingBlockDistance = list(np.arange(selectedOptionBlock[1],
                                            selectedOptionBlock[1] + (selectedOptionBlock[0]) * selectedOptionBlock[2],
                                            selectedOptionBlock[2]))

        self.listBlockDistance = list(np.concatenate([increasingBlockDistance, np.flip(decreasingBlockDistance)]))

    # Method to create the blocks
    # The method here is pretty simple: we create an increasing block distance and we mirror the blocks
    def createBlocks(self):

        # STEP 1: We need to create an Increasing Set

        # We first create an Increasing/Decreasing Set based on the increasing block distance
        # Note: Here it is important to ensure that standardInit = False to avoid recreating the distance. 
        increasingSet = IncreasingDecreasingDistanceSet(distance=np.sum(self.increasingBlockDistance),
                                                        standardInit=False,
                                                        neutralSegment=self.neutralSegment,
                                                        focusSegment=self.focusSegment)

        # We then need to force the block distance list &  the type (increase)
        increasingSet.listBlockDistance = np.flip(self.increasingBlockDistance) # Note: we reverse it as by defualt, the IncreaseDecreaseSet takes a decreasing distance pattern
        increasingSet.increaseDecrease = "increase"

        # The sequence type can then be determined "normally"
        increasingSet.setSequenceType()

        # Finally the blocks of the set can be created by using the normal function
        increasingSet.createBlocks() # Tis is when the bocks and distances will be flipped as this is an "increase" set

        # Just storing the increasing set for quality control ;-) 
        self.increasingSet = increasingSet

        # STEP 2: We then populate each Attribute of the pyramid set class

        # listBlocks & listBlockDistance
        listBlockDistance = list(increasingSet.listBlockDistance.copy())
        listBlock = list(increasingSet.listBlock.copy())
        nBlocks = len(listBlock)
        for i in np.arange(nBlocks-1):
            listBlockDistance.append(listBlockDistance[nBlocks-2-i])
            listBlock.append(listBlock[nBlocks-2-i])
        self.listBlockDistance = listBlockDistance
        self.listBlock = listBlock

        # Variation Segment: Not populated

        # sequence Type
        self.sequenceType = increasingSet.sequenceType
