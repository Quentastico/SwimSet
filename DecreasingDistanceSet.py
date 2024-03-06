## GLOBAL VARIABLES

import numpy as np
import globals
from utils import splitSetIncreaseDecrease
from Block import Block
from Set import Set
from Variation import Variation
import utils

class DecreasingDistanceSet(Set):

    # Object initialisation
    def __init__(self, distance):

        super().__init__(distance)

        self.sequenceType = "" # This attribute will contain the type of sequence

    # Method to split the set into a given distance
    def setBlockDistances(self): 

        # Finding all the ways to cut the set
        optionBlocks = splitSetIncreaseDecrease(distance = self.distance,
                                                stepBlockDistance = globals.stepBlockDistance,
                                                minBlockDistance = globals.minBlockDistance,
                                                minBlocks = globals.minBlocksIncrease)

        # Choosing a random way
        selectedOptionBlock = optionBlocks[np.random.randint(low=0, high=len(optionBlocks))]
        
        # Constracting the distances of the blocks withtin the set
        self.listBlockDistance = np.flip(np.arange(selectedOptionBlock[1], selectedOptionBlock[1] + (selectedOptionBlock[0]) * selectedOptionBlock[2], selectedOptionBlock[2]))

    # Method to select the type of sequence
    def setSequenceType(self):

        # Just picking a random type from available options
        self.sequenceType = np.random.choice(globals.splitTypeIncreaseDecreaseDistance, p=globals.splitProbaIncreaseDecreaseDistance)
    
    # Method to create the blocks of the set
    def createBlocks(self):

        # Case 1: Only one subsegment per block
        if self.sequenceType == "singleSegment":

            # We first need to create the first block
            firstBlock = Block(distance=self.listBlockDistance[0], nSegments=1)
            firstBlock.setSegmentDistances()
            firstBlock.createSegments()

            # We then duplicate the first block by changing uniquely the distance
            for blockDistance in self.listBlockDistance:
                newBlock = firstBlock.copy()
                newBlock.listSegmentDistance = [blockDistance]
                newBlock.listSegment[0].distance = blockDistance
                self.listBlock.append(newBlock)

            # We then determine what can change from one block to another 
            varyingParameters = firstBlock.listSegment[0].getVaryingParameters()

            # We then select the parameter that will change and its values through the creation of a variation
            variationSegment = Variation(allowedVariation=globals.allowedVariationIncreaseDecreaseDistance1, varyingParameters=varyingParameters, nBlocks=len(self.listBlockDistance))
            variationSegment.selectParameter()
            variationSegment.createVariation()
            self.variationSegment = variationSegment

            # We then change the relevant parameter in the blocks
            if variationSegment.selParameter is not None:
                indexBlock = 0
                for block in self.listBlock:
                    block.listSegment[0].setForcedParameter(parameterName=variationSegment.selParameter, parameterValue=variationSegment.selParameterVariation[indexBlock])
                    indexBlock += 1