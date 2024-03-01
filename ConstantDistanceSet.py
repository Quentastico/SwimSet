## IMPORTS

import numpy as np
import globals
from Block import Block
from Set import Set
from Variation import Variation
import utils

class ConstantDistanceSet(Set):

    # Object initialisation
    def __init__(self, distance):
        super().__init__(distance)

    # Method to split the set into a given distance
    def setBlockDistances(self): 

        optionDistanceBlock = []

        for distance in np.arange(globals.minBlockDistance, self.distance + globals.stepBlockDistance, globals.stepBlockDistance):
            if self.distance / distance == np.floor(self.distance / distance):
                optionDistanceBlock.append(distance)

        # Setting then randomly the distance
        blockDistance = optionDistanceBlock[np.random.randint(low=0, high=len(optionDistanceBlock))]

        # Finally setting the list of distance blocks
        for i in np.arange(int(self.distance / blockDistance)):
            self.listBlockDistance.append(blockDistance)

    # Method to create the blocks and the segments composing each block
    def createBlocks(self): 

        # 1. We need to define what sequence of blocks we will have:
        # Case 1: The block will have a random number of segments that will simply repeat from one block to the other
        # Case 2: The block will have exactly two segments that will vary according to an increasing or decreasing pattern (if possible)

        sequenceBlocks = np.random.choice(globals.splitTypeConstantDistance, p=globals.splitProbaConstantDistance)
        print(sequenceBlocks)

        # 2. We then need to create the segments composing each block

        # 2.1. Case 1: Random number of segments
        if sequenceBlocks == "randomSplit":

            # We create the first block
            firstBlock = Block(distance=self.listBlockDistance[0])

            # Then we use the functionality to randomly split the block into segments of different distances
            firstBlock.setSegmentDistances()

            # We then create the blocks composing the segment by calling the appropriate Block method
            firstBlock.createSegments()

            # We then decide which segment will change from one block to the other
            changingSegmentIndex = np.random.randint(0, len(firstBlock.listSegment))
            changingSegment = firstBlock.listSegment[changingSegmentIndex]

            # We then copy the first block as many times as necessary
            for blockDistance in self.listBlockDistance:
                newBlock = firstBlock.copy()
                self.listBlock.append(newBlock)

            # We then determine the parameter than will vary from one block to the other in the changing block
            varyingParameters = changingSegment.getVaryingParameters()
            print(varyingParameters)
            print(globals.allowedVariationConstantDistance1)
            print(len(self.listBlockDistance))

            # We then create a variation for this changing segment
            variationSegment = Variation(allowedVariation=globals.allowedVariationConstantDistance1, varyingParameters=varyingParameters, nBlocks=len(self.listBlockDistance))
            variationSegment.selectParameter()
            variationSegment.createVariation()
            self.variationSegment = variationSegment

            # We then change the value of the changing parameter of the changing segment from one block to the other. 
            indexBlock = 0
            for block in self.listBlock:
                block.listSegment[changingSegmentIndex].setForcedParameter(parameterName=variationSegment.selParameter, parameterValue=variationSegment.selParameterVariation[indexBlock])
                indexBlock += 1




            




