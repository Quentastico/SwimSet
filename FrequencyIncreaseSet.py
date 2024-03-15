## IMPORTS
import numpy as np
import globals
from utils import splitSetFrequencyIncrease
from Block import Block
from Set import Set
from Segment import Segment
from Variation import Variation

class FrequencyIncreaseSet(Set):

    # Object initialisation
    def __init__(self, distance, standardInit=False):

        super().__init__(distance=distance, standardInit=standardInit)

        self.type = "Frequency Increase"
        self.selCombo = [] # The combination that is reatined, in the format n, d, where n is the number of segments in a bunch and d is the segment length

        if self.standardInit:
            self.setBlockDistances()
            self.createBlocks()

    # Method to determine the specific distance combo
    def setBlockDistance(self):

        # 1. We first need to get all the possible scores by using the appropriate utils function
        optionCombos, scores = splitSetFrequencyIncrease(distance=self.distance,
                                                         stepBlockDistance=globals.stepBlockDistance,
                                                         minBlockDistance=globals.minBlockDistance,
                                                         maxBlockDistance=globals.maxBlockDistance,
                                                         minN=globals.minNumberFrequencyIncrease,
                                                         maxN=globals.maxNumberFrequencyIncrease,
                                                         maxDistanceDiff=globals.maxDistanceDiff)
        
        # 2. We then need to select a combo
        if len(optionCombos) == 0:
            print("It is not possible to find a frequency Increase set for this one - pick another type of set for this distance or change the distance")
            self.selCombo = None
            self.listBlockDistance = None

        else: 
            probaCombos = scores/sum(scores)
            selComboIndex = np.random.choice(np.arange(len(optionCombos)), p=probaCombos)
            self.selCombo = optionCombos[selComboIndex]

        # 3. Then we determine the size of each block
        if self.selCombo is not None:

            n = self.selCombo[0]
            d = self.selCombo[1]
            for i in np.arange(n):
                self.listBlockDistance.append(n * (n-i) * d)

    # Method to create the blocks
    def createBlocks(self):

        # 1. First we create a "base segment", which will be random
        baseSegment = Segment(distance=self.selCombo[1])
        baseSegment.setRandomAll()

        # 2. Then we determine what can vary from this segment
        varyingParameters = baseSegment.getVaryingParameters()

        # 3. We then create a variation that will determine hat parameters will actually change from the base segment to the special segment
        variationSegment = Variation(allowedVariation=globals.allowedVariationFrequencyIncrease1, 
                                     varyingParameters=varyingParameters, 
                                     nBlocks=2, 
                                     standardInit=True)
        self.variationSegment = variationSegment

        # 4. We then change the value of baseSegment parameter which is supposed to change
        baseSegment.setForcedParameter(parameterName=variationSegment.selParameter, parameterValue=variationSegment.selParameterVariation[0])

        # 5. We then create the special Segment
        specialSegment = baseSegment.copy()
        specialSegment.setForcedParameter(parameterName=variationSegment.selParameter, parameterValue=variationSegment.selParameterVariation[1])

        # 6. We then need to create the blocks "from scratch" by collating the baseSegment and the specialSegment at a given frequency

        # 6.1. Extracting the useful combo parameters
        n = self.selCombo[0]
        d = self.combo[1]

        # 6.2. Looping all all the blocks
        for blockDistance in self.listBlockDistance:

            # Calculating the number of segments in this block
            nSegments = int(blockDistance/d)

            # Creating the block and setting the list of segment distance within the block
            newBlock = Block(distance=blockDistance, nSegments=nSegments)
            newBlock.setSegmentDistances()

            # Then we create the "subblock" which contains a total of nSegment/n segments
            subBlocks = []
            for i in np.arange(int(nSegments/n)-1):
                subBlocks.append(baseSegment)
            subBlocks.append(specialSegment)

            # We then repeat the subBlock n times in the Block
            for i in np.arange(n):
                newBlock.listSegment.append(subBlocks)








        
