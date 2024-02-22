## GLOBAL VARIABLES

import numpy as np
import globals
from Block import Block
from Set import Set
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

    
