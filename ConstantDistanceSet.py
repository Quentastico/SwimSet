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

        self.sequenceType = "" # This attribute contains the type of sequence: randomSplit, increasedecreaseSplit
        self.listSegmentDistance = [] # This attribute will contain a list of the list of segment distances withtin each block

    # Method to split the set into a given distance
    def setBlockDistances(self): 

        # Here the idea is to store in two different arrays the different options for the distance sequence
        # optionRandomSplit: this array will simply contain the value of the possible block distances in the sace of a random split
        # optionIncreaseDecreaseSplit: this array of arrays contains the series of possible distances for the segments

        optionRandomSplit = []
        optionIncreaseDecreaseSplit = {}

        # Loop over all possible distances for the constant blocks
        for distance in np.arange(globals.minBlockDistance, self.distance + globals.stepBlockDistance, globals.stepBlockDistance):
            
            # Condition: the number of blocks is an integer
            nBlocks = self.distance / distance
            if nBlocks == np.floor(nBlocks):

                optionRandomSplit.append(distance)

                if nBlocks >2:

                    # Extra condition: we need to be able to split the distance in a logical way for the segments
                    if distance/nBlocks/globals.minSegmentDistance == np.floor(distance/nBlocks/globals.minSegmentDistance):
                        optionIncreaseDecreaseSplit[distance] = np.arange(start=distance/nBlocks, stop=(nBlocks+1)*distance/nBlocks, step=distance/nBlocks)

                    # We also accept cases where we add a "0" at the start of the sequence
                    if nBlocks != 1:
                        if distance/(nBlocks-1)/globals.minSegmentDistance == np.floor(distance/(nBlocks-1)/globals.minSegmentDistance):
                            optionIncreaseDecreaseSplit[distance] = np.arange(start=0, stop=(nBlocks)*distance/(nBlocks-1), step=distance/(nBlocks-1)) 

        # Then deciding what type of Block sequence this will be: 
            # randomSplit: The block will have a random number of segments that will simply repeat from one block to the other
            # increaseDecreaseSplit: The block will have exactly two segments that will vary according to an increasing or decreasing pattern (if possible)
        
        if len(optionIncreaseDecreaseSplit.keys())>0:
            self.sequenceType = np.random.choice(globals.splitTypeConstantDistance, p=globals.splitProbaConstantDistance)
        else: 
            self.sequenceType = "randomSplit"

        # Then picking a random distance for the block
        if self.sequenceType == "randomSplit":
            # Picking a random distance in the array
            blockDistance = optionRandomSplit[np.random.randint(low=0, high=len(optionRandomSplit))]
            # Then creating an array of distances for the blocks and segment
            for i in np.arange(int(self.distance / blockDistance)):
                self.listBlockDistance.append(blockDistance)
                self.listSegmentDistance.append(blockDistance)            

        if self.sequenceType == "increaseDecreaseSplit":
            # Picking a random distance in the array
            possibleDistances = list(optionIncreaseDecreaseSplit.keys())
            blockDistance = possibleDistances[np.random.randint(low=0, high=len(possibleDistances))]
            # Then creating an array of distances
            for i in np.arange(int(self.distance / blockDistance)):
                self.listBlockDistance.append(blockDistance)
                self.listSegmentDistance.append([optionIncreaseDecreaseSplit[blockDistance][i], blockDistance-optionIncreaseDecreaseSplit[blockDistance][i]])

    # Method to create the blocks and the segments composing each block
    def createBlocks(self): 

        # 1. Case 1: Random number of segments
        if self.sequenceType == "randomSplit":

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




            




