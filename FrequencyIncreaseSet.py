## IMPORTS
import numpy as np
import globals
from utils import splitSetFrequencyIncrease
from Block import Block
from Set import Set
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

        
