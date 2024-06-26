## IMPORTS
import numpy as np
from utils import splitSetFrequencyIncrease
from Block import Block
from Set import Set
from Segment import Segment
from Variation import Variation
import settings

class FrequencyIncreaseSet(Set):

    # Object initialisation
    def __init__(self, distance, standardInit=False, neutralSegment=None, focusSegment=None, verbose=0):

        super().__init__(distance=distance, standardInit=standardInit, neutralSegment=neutralSegment, focusSegment=focusSegment, verbose=verbose)

        self.type = "Frequency Increase"
        self.selCombo = [] # The combination that is reatined, in the format n, d, where n is the number of segments in a bunch and d is the segment length

        if self.standardInit:

            # Defining the distance list of this block in the set
            self.setBlockDistances()

            # Then making sure that the distance list for the block has been defined
            if self.listBlockDistance is not None: 
                self.createBlocks()
                self.finalise()

    # Method to determine the specific distance combo
    def setBlockDistances(self):

        # 1. We first need to get all the possible scores by using the appropriate utils function
        optionCombos, scores = splitSetFrequencyIncrease(distance=self.distance,
                                                         stepBlockDistance=settings.globals.stepBlockDistance,
                                                         minBlockDistance=settings.globals.minBlockDistance,
                                                         maxBlockDistance=settings.globals.maxBlockDistance,
                                                         minN=settings.globals.minNumberFrequencyIncrease,
                                                         maxN=settings.globals.maxNumberFrequencyIncrease,
                                                         maxDistanceDiff=settings.globals.maxDistanceDiff)
        
        # 2. We then need to select a combo
        if len(optionCombos) == 0:
            if self.verbose>0:
                print("It is not possible to find a frequency Increase set for this one - pick another type of set for this distance or change the distance")
            self.selCombo = None
            self.listBlockDistance = []

        else: 
            probaCombos = scores/sum(scores)
            selComboIndex = np.random.choice(np.arange(len(optionCombos)), p=probaCombos)
            self.selCombo = optionCombos[selComboIndex]

        # 3. Then we determine the size of each block
        if self.selCombo is not None:
            n = self.selCombo[0]
            d = self.selCombo[1]
            for i in np.arange(int(0.5*(np.power(n,2) + np.power(n,3)))):
                self.listBlockDistance.append(d)

    # Method to create the blocks
    def createBlocks(self):

        # In a first part of the code, we will aime to create the "base segment" and the "special segment"
        # The base segment will repeat multiple times
        # The special segment will not repeat as often, but will be the focus of the swimmer
        # Note that these will be contained in blocks of single segments
        # We have two ways to generate these two segments
        # Either randomly 
        # Or according to a meta-pattern if we are in a meta set

        # Case of the random defintiion of the two segments
        if self.neutralSegment is None: 

            # 1. First we create a "base" segment, which will be random
            baseSegment = Segment(distance=self.selCombo[1])
            baseSegment.setRandomAll()

            # Note that we need to remove the pullBuoyandPaddles and drill options for this one 
            # as otherwise there won't be any option for a variation
            if baseSegment.equipment == "pullBuoyAndPaddles":
                baseSegment.setForcedParameter(parameterName="equipment", parameterValue="No equipment")
            if baseSegment.drill == "drill":
                baseSegment.setForcedParameter(parameterName="drill", parameterValue = "No drill")

            # 2. Then we determine what can vary from this segment
            varyingParameters = baseSegment.getVaryingParameters()

            # 3. We then create a variation that will determine what parameters will actually change from the base segment to the special segment
            variationSegment = Variation(allowedVariation=settings.globals.allowedVariationFrequencyIncrease1, 
                                        varyingParameters=varyingParameters, 
                                        nBlocks=2, 
                                        standardInit=True)
            self.variationSegment = variationSegment

            # 4. We then change the value of baseSegment parameter which is supposed to change
            baseSegment.setForcedParameter(parameterName=variationSegment.selParameter, parameterValue=variationSegment.selParameterVariation[0])

            # 5. We then create the special Segment
            specialSegment = baseSegment.copy()
            specialSegment.setForcedParameter(parameterName=variationSegment.selParameter, parameterValue=variationSegment.selParameterVariation[1])

            # 6. We then apply to the base segment the constraints created by the newly created special segment
            constraintBaseSegment = specialSegment.getBaseSegmentParameters(selParameter=variationSegment.selParameter)
            for parameter in constraintBaseSegment:
                baseSegment.setForcedParameter(parameterName=parameter, parameterValue=constraintBaseSegment[parameter])

        # Case of a meta-set: the two segments are defined by neutralSegment and focusSegment
        else:

            # Base segment: set by neutralSegment characteristics
            baseSegment = Segment(distance=self.selCombo[1])
            for parameter in settings.globals.listAllParameters:
                baseSegment.setForcedParameter(parameterName=parameter,
                                               parameterValue=self.neutralSegment[parameter])
                
            # Special segment: set by the focusSegment characteristics
            specialSegment = baseSegment.copy()
            for parameter in settings.globals.listAllParameters:
                specialSegment.setForcedParameter(parameterName=parameter,
                                                  parameterValue=self.focusSegment[parameter])
        
        # 7. We then "mark" specialSegment as the focus one
        specialSegment.focus = True

        # 8. We then need to create the blocks "from scratch" by collating the baseSegment and the specialSegment at a given frequency

        # 8.1. Extracting the useful combo parameters
        n = self.selCombo[0]
        d = self.selCombo[1]

        # 8.2. then creating the two blocks of interest
        baseBlock = Block(distance=d, nSegments=1)
        baseBlock.listSegmentDistance = [d]
        baseBlock.listSegment = [baseSegment.copy()]

        specialBlock = Block(distance=d, nSegments=1)
        specialBlock.listSegmentDistance = [d]
        specialBlock.listSegment = [specialSegment.copy()]

        # Here we are looping on the total number of meta-blocks
        # The first meta-bloc will have n*n segments
        # The second meta-block will have n*(n-1) segments
        # ...
        # The last meta blocks will have n segments
        for i in np.arange(n, 0, -1):

            for _ in np.arange(n):

                for p in np.arange(i):

                    # Test to determine if this is a focus one
                    if np.floor((p+1)/i) == (p+1)/i:
                        self.listBlock.append(specialBlock.copy())
                    else: 
                        self.listBlock.append(baseBlock.copy())

