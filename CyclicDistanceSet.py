## IMPORTS

import numpy as np
import globals
from utils import splitSetCyclicDistance
from IncreasingDecreasingDistanceSet import IncreasingDecreasingDistanceSet
from Block import Block
from Set import Set

class CyclicDistanceSet(Set):

    # Object initialisation
    def __init__(self, distance, standardInit=False, neutralSegment=None, focusSegment=None):

        super().__init__(distance, standardInit=standardInit, neutralSegment=neutralSegment, focusSegment=focusSegment)

        self.type = "Cyclic Distance"
        self.selCombo = [] # Parameter of the selected distance combo

        if self.standardInit:
            self.setBlockDistances()

    # Method to set the block distances
    def setBlockDistances(self):

        # Create a way to split the set
        combos = splitSetCyclicDistance(distance=self.distance,
                                        minBlockDistance=globals.minBlockDistance,
                                        maxBlockDistance=globals.maxBlockDistance,
                                        stepBlockDistance=globals.stepBlockDistance)
        
        
        if len(combos) > 0:

            # Selecting a random combo
            selComboIndex = np.random.choice(np.arange(len(combos)))
            selCombo = combos[selComboIndex]

            # Creating the distance list for the selected combo
            d = selCombo[0]
            s = selCombo[1]
            n = selCombo[2]
            N = selCombo[3]

            # Creating the first series
            series = []
            for i in np.arange(n+1):
                series.append(int(d + i*s))

            # Adding N series
            for i in np.arange(N):
                self.listBlockDistance += series

        else:

            print("There is no distance combo possible for this type of set (Cyclic Distance)")

    

    
