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
        # Note: it must be ensured that for the "half-half" scheme to be selected, half of the minimal block distance is higher than the minimal segment distance
        
        if np.min(self.listBlockDistance)/2 >= globals.minSegmentDistance:
            self.sequenceType = np.random.choice(globals.splitTypeIncreaseDecreaseDistance, p=globals.splitProbaIncreaseDecreaseDistance)
        else:
            splitType = globals.splitTypeIncreaseDecreaseDistance.copy()
            splitProba = globals.splitProbaIncreaseDecreaseDistance.copy()
            halfHalfIndex = splitType.index("halfHalf")
            splitType.remove("halfHalf")
            splitProba.pop(halfHalfIndex)
            newSumProba = np.sum(splitProba)
            for i in np.arange(len(splitProba)):
                splitProba[i] = splitProba[i]/newSumProba
            self.sequenceType = np.random.choice(splitType, p=splitProba)


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
                newBlock.distance = blockDistance
                newBlock.listSegmentDistance = [blockDistance]
                newBlock.listSegment[0].distance = blockDistance
                self.listBlock.append(newBlock)

            # We then determine what can change from one block to another 
            varyingParameters = firstBlock.listSegment[0].getVaryingParameters()

            # We then select the parameter that will change and its values through the creation of a variation
            variationSegment = Variation(allowedVariation=globals.allowedVariationIncreaseDecreaseDistance2, varyingParameters=varyingParameters, nBlocks=len(self.listBlockDistance))
            variationSegment.selectParameter()
            variationSegment.createVariation()
            self.variationSegment = variationSegment

            # We then change the relevant parameter in the blocks
            if variationSegment.selParameter is not None:
                indexBlock = 0
                for block in self.listBlock:
                    block.listSegment[0].setForcedParameter(parameterName=variationSegment.selParameter, parameterValue=variationSegment.selParameterVariation[indexBlock])
                    indexBlock += 1

        # Case 2: "Half-half"
        if self.sequenceType=="halfHalf":

            # We first need to create a first block and we make sure the distance of its segments are equal to half-half of the block distance
            firstBlock = Block(distance=self.listBlockDistance[0], nSegments=2)
            segmentDistance = int(self.listBlockDistance[0]/2)
            firstBlock.listSegmentDistance = [segmentDistance, segmentDistance]

            # We then create the segments of this first block
            firstBlock.createSegments()
            firstBlock.info()

            # We then duplicate the first block by changing the distance of its segments
            print("new blocks")
            for distance in self.listBlockDistance:
                newBlock = firstBlock.copy()
                newBlock.distance = distance
                segmentDistance = int(distance/2)
                newBlock.listSegmentDistance = [segmentDistance, segmentDistance]
                newBlock.listSegment[0].distance = segmentDistance
                newBlock.listSegment[1].distance = segmentDistance
                self.listBlock.append(newBlock)
            
            # We then need to decide what segment will vary from one block to the other
            changingSegmentIndex = np.random.randint(0, 2)

            # Then we need to determine what parameters can vary from one block to the other from this segment
            varyingParameters = firstBlock.listSegment[changingSegmentIndex].getVaryingParameters()

            # We then select the parameter that will change and its values through the creation of a variation
            variationSegment = Variation(allowedVariation=globals.allowedVariationIncreaseDecreaseDistance2, varyingParameters=varyingParameters, nBlocks=len(self.listBlockDistance))
            variationSegment.selectParameter()
            variationSegment.createVariation()
            self.variationSegment = variationSegment

            # We then change the relevant parameter in the blocks
            if variationSegment.selParameter is not None:
                indexBlock = 0
                for block in self.listBlock:
                    block.listSegment[0].setForcedParameter(parameterName=variationSegment.selParameter, parameterValue=variationSegment.selParameterVariation[indexBlock])
                    indexBlock += 1

        # Case 3: constant bit + changing bit
        if self.sequenceType == "constantChanging":

            # We first need to create a random block with two segments
            firstBlock = Block(distance=self.listBlockDistance[0], nSegments=2)
            firstBlock.setSegmentDistances()
            firstBlock.createSegments()
            print("first block")
            firstBlock.info()

            # We then duplicate the first block to allow for a block with a constant part (the last part) and a changing part
            constantDistance = np.min(self.listBlockDistance)
            for distance in self.listBlockDistance:
                changingDistance = distance - constantDistance
                # Case for the first blocks (with two segments)
                if changingDistance > 0: 
                    newBlock = firstBlock.copy()
                    newBlock.distance = distance
                    newBlock.listSegmentDistance = [changingDistance, constantDistance]
                    newBlock.listSegment[0].distance = changingDistance
                    newBlock.listSegment[1].distance = constantDistance
                # Case for the last block
                else: 
                    newBlock = Block(distance=constantDistance, nSegments=1)
                    newBlock.listSegmentDistance = [constantDistance]
                    newBlock.listSegment = [firstBlock.listSegment[1].copy()]
                    newBlock.listSegment[0].distance = constantDistance
                self.listBlock.append(newBlock)
                print("new block!")
                newBlock.info()
            
            # We then determine the parameters that can vary for the first segment
            varyingParameters = firstBlock.listSegment[0].getVaryingParameters()

            # We then determine the parameter that will actually vary from one block to the other through the creation of a Variation
            variationSegment = Variation(allowedVariation=globals.allowedVariationIncreaseDecreaseDistance3, varyingParameters=varyingParameters, nBlocks=len(self.listBlockDistance))
            variationSegment.selectParameter()
            variationSegment.createVariation()
            self.variationSegment = variationSegment

            # We then modify the first segment accordingly
            if variationSegment.selParameter is not None:
                indexBlock = 0
                for block in self.listBlock[:-1]:
                    block.listSegment[0].setForcedParameter(parameterName=variationSegment.selParameter, parameterValue=variationSegment.selParameterVariation[indexBlock])
                    indexBlock += 1
            
            # We then choose to flip or not the order of the segment in each block
            flip = np.random.choice([True, False])
            if flip:
                for block in self.listBlock:
                    block.flip()
            


