## IMPORTS

import numpy as np
from Block import Block
from Set import Set
from Variation import Variation
import utils
import settings

class ConstantDistanceSet(Set):

    # Object initialisation
    def __init__(self, distance, standardInit=False, neutralSegment=None, focusSegment=None, verbose=0):

        super().__init__(distance=distance, standardInit=standardInit, neutralSegment=neutralSegment, focusSegment=focusSegment, verbose=verbose)

        self.type = "Constant Distance"
        self.listSegmentDistance = [] # This attribute will contain a list of the list of segment distances within each block

        if self.standardInit:
            self.setBlockDistances()
            self.createBlocks()
            self.finalise()

    # Method to split the set into a given distance
    def setBlockDistances(self): 

        # Here the idea is to store in two different arrays the different options for the distance sequence
        # optionRandomSplit: this array will simply contain the value of the possible block distances in the sace of a random split
        # optionIncreaseDecreaseSplit: this array of arrays contains the series of possible distances for the segments

        optionRandomSplit = []
        optionIncreaseDecreaseSplit = {}

        # Loop over all possible distances for the constant blocks
        for distance in np.arange(settings.globals.minBlockDistance, self.distance + settings.globals.stepBlockDistance, settings.globals.stepBlockDistance):
            
            # Condition: the number of blocks is an integer
            nBlocks = self.distance / distance
            if nBlocks == np.floor(nBlocks):

                optionRandomSplit.append(distance)

                if nBlocks >2:

                    # Extra condition: we need to be able to split the distance in a logical way for the segments
                    if distance/nBlocks/settings.globals.minSegmentDistance == np.floor(distance/nBlocks/settings.globals.minSegmentDistance):
                        optionIncreaseDecreaseSplit[distance] = np.arange(start=distance/nBlocks, stop=int((nBlocks+1)*distance/nBlocks), step=int(distance/nBlocks), dtype=int)

                    # We also accept cases where we add a "0" at the start of the sequence
                    if nBlocks != 1:
                        if distance/(nBlocks-1)/settings.globals.minSegmentDistance == np.floor(distance/(nBlocks-1)/settings.globals.minSegmentDistance):
                            optionIncreaseDecreaseSplit[distance] = np.arange(start=0, stop=int((nBlocks)*distance/(nBlocks-1)), step=int(distance/(nBlocks-1)), dtype=int) 

        # Then deciding what type of Block sequence this will be: 
            # randomSplit: The block will have a random number of segments that will simply repeat from one block to the other
            # increaseDecreaseSplit: The block will have exactly two segments that will vary according to an increasing or decreasing pattern (if possible)
        
        if len(optionIncreaseDecreaseSplit.keys())>0:
            self.sequenceType = np.random.choice(settings.globals.splitTypeConstantDistance, p=settings.globals.splitProbaConstantDistance)
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
            nonChangingSegmentIndexes = np.delete(np.arange(len(firstBlock.listSegment)), changingSegmentIndex)
            changingSegment = firstBlock.listSegment[changingSegmentIndex]

            # We then copy the first block as many times as necessary
            for blockDistance in self.listBlockDistance:
                newBlock = firstBlock.copy()
                self.listBlock.append(newBlock)

            # First case: this set is not part of a meta set: here we create a variation and change a single parameter in a segment from one block
            # to the other
            
            if self.neutralSegment is None: 

                # We then determine the parameter than will vary from one block to the other in the changing block
                varyingParameters = changingSegment.getVaryingParameters()

                # We then create a variation for this changing segment
                variationSegment =  Variation(allowedVariation=settings.globals.allowedVariationConstantDistance1,
                                            varyingParameters=varyingParameters,
                                            nBlocks=len(self.listBlockDistance),
                                            standardInit=True)
                self.variationSegment = variationSegment

                # We then change the value of the changing parameter of the changing segment from one block to the other. 
                # We also need to change the value of the other segments is there is any constraint brought by the changing segment
                # Note this second change (on the non-changing segments) needs to happen here as for each block, the constraint may change ("same" values)
                if variationSegment.selParameter is not None:
                    
                    indexBlock = 0
                    for block in self.listBlock:
                        
                        # Changing segment in the block
                        block.listSegment[changingSegmentIndex].setForcedParameter(parameterName=variationSegment.selParameter,
                                                                                parameterValue=variationSegment.selParameterVariation[indexBlock])
                        
                        # Then marking the changing segment as the "focus segment"
                        block.listSegment[changingSegmentIndex].focus = True
                        
                        # Then determining the constraints on the non-changing segments
                        constraintBaseSegment = block.listSegment[changingSegmentIndex].getBaseSegmentParameters(variationSegment.selParameter)
                        
                        # Non changing segment(s) in the block
                        for indexSegment in nonChangingSegmentIndexes:

                            # Applying the constratint(s), if any, on the other segments
                            for parameter in constraintBaseSegment.keys():

                                block.listSegment[indexSegment].setForcedParameter(parameterName=parameter,
                                                                                   parameterValue=constraintBaseSegment[parameter])

                        indexBlock += 1
            
            else: 

                # We need to loop in all the block of the set
                # The changing segment will be forced to have all the characetristics of the focus segments; 
                # all the others will have the values of the neutral segment

                for block in self.listBlock:

                    for parameter in settings.globals.listAllParameters:

                        # Changing the values of the focus segment
                        block.listSegment[changingSegmentIndex].setForcedParameter(parameterName=parameter,
                                                                                   parameterValue=self.focusSegment[parameter])
                        
                        # Then marking the changing segment as the "focus segment"
                        block.listSegment[changingSegmentIndex].focus = True
                        
                        # Changing the values of the neutral segment(s)
                        for indexSegment in nonChangingSegmentIndexes:
                            block.listSegment[indexSegment].setForcedParameter(parameterName=parameter,
                                                                               parameterValue=self.neutralSegment[parameter])

        # 2. Case 2: Increase/decrease split
        if self.sequenceType == "increaseDecreaseSplit":

            # We first create the first Block - Note that we need to force the number of segment nSegments to 2 and the list of segment distances
            firstBlock = Block(distance=self.listBlockDistance[0], nSegments=2)
            firstBlock.listSegmentDistance = self.listSegmentDistance[0]

            # We then create the segments withtin the same Block 
            firstBlock.createSegments()

            # We then need to copy the firstBlock, but this time by changing the distances of its segments
            for i in np.arange(len(self.listBlockDistance)):
                newBlock = firstBlock.copy()
                newBlock.listSegmentDistance = self.listSegmentDistance[i]
                newBlock.listSegment[0].distance = self.listSegmentDistance[i][0]
                newBlock.listSegment[1].distance = self.listSegmentDistance[i][1]
                self.listBlock.append(newBlock)
            
            # We then decide which segment will change from one block to the other
            # - If this is the first one, then the distance of the changing segment will increase within the set (case 2.1)
            # - In the other case, the distance of the changing segment will decrease within the set (case 2.1)
            changingSegmentIndex = np.random.randint(0, 2)
            nonChangingSegmentIndex = np.delete(np.arange(2), changingSegmentIndex)[0]
            changingSegment = firstBlock.listSegment[changingSegmentIndex]

            # Then we have two cases: 
            # Either this is not a meta set: the variation will be random
            # Or we are in a meta set: the changing segment will be the same each time and dicated by the focusSegment characteristics

            if self.neutralSegment is None: 

                if changingSegmentIndex == 0:
                    allowedVariationConstantDistance = settings.globals.allowedVariationConstantDistance21
                else: 
                    allowedVariationConstantDistance = settings.globals.allowedVariationConstantDistance22

                # We then determine the parameter than can vary from one block to the other in the changing block
                varyingParameters = changingSegment.getVaryingParameters()
                
                # We then determine what parameter will actually vary from one block to the other through the creation of a Variation
                variationSegment =  Variation(allowedVariation=allowedVariationConstantDistance,
                                            varyingParameters=varyingParameters,
                                            nBlocks=len(self.listBlockDistance),
                                            standardInit=True)
                self.variationSegment = variationSegment                

                # We finally adjust the changing segment withtin the block
                if variationSegment.selParameter is not None:

                    indexBlock = 0

                    for block in self.listBlock:

                        # changing segment
                        block.listSegment[changingSegmentIndex].setForcedParameter(parameterName=variationSegment.selParameter,
                                                                                   parameterValue=variationSegment.selParameterVariation[indexBlock])
                        
                        # Then marking the changing segment as the "focus segment"
                        block.listSegment[changingSegmentIndex].focus = True

                        # Then determining the constraints on the non-changing segments
                        constraintBaseSegment = block.listSegment[changingSegmentIndex].getBaseSegmentParameters(variationSegment.selParameter)

                        # Non-changing segment
                        for parameter in settings.globals.listAllParameters:

                            block.listSegment[nonChangingSegmentIndex].setForcedParameter(parameterName=parameter,
                                                                                        parameterValue=constraintBaseSegment[parameter])

                        indexBlock += 1

            else: 

                # We need to loop in all the block of the set
                # The changing segment will be forced to have all the characetristics of the focus segments; 
                # all the others will have the values of the neutral segment

                for block in self.listBlock:

                    for parameter in settings.globals.listAllParameters:

                        # Changing the values of the focus segment
                        block.listSegment[changingSegmentIndex].setForcedParameter(parameterName=parameter,
                                                                                   parameterValue=self.focusSegment[parameter])
                        
                        # Then marking the changing segment as the "focus segment"
                        block.listSegment[changingSegmentIndex].focus = True
                        
                        # Changing the values of the neutral segment(s)
                        block.listSegment[nonChangingSegmentIndex].setForcedParameter(parameterName=parameter,
                                                                                      parameterValue=self.neutralSegment[parameter])

            # Finally in this block, we need to remove segments which have a distance of 0m
            for block in self.listBlock:   

                for segment in block.listSegment: 

                    if segment.distance == 0:
                        block.listSegment.remove(segment)
                        block.listSegmentDistance.remove(segment.distance)
                        block.nSegments -= 1

            # And then, just to keep things 100% clean, we also remove the null values in the listSegmentDistance
            for item in self.listSegmentDistance:
                for element in item:
                    if element == 0:
                        item.remove(element)             
            