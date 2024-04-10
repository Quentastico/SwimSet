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
        self.series = [] # This will contain the first "series" in the cyclic set 
                         # (for example, if the full set is 100 - 200 - 100 - 200, the series is [100, 200])

        if self.standardInit:
            self.setBlockDistances()
            self.createBlocks()
            self.finalise()

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
            self.selCombo = selCombo

            # Creating the distance list for the selected combo
            d = selCombo[0]
            s = selCombo[1]
            n = selCombo[2]
            N = selCombo[3]

            # Creating the first series
            series = []
            for i in np.arange(n+1):
                series.append(int(d + i*s))
            self.series = series

            # Adding N series
            for i in np.arange(N):
                self.listBlockDistance += series

        else:

            print("There is no distance combo possible for this type of set (Cyclic Distance)")

    # Method to create the blocks
    def createBlocks(self):

        # Here the startegy consists of creating an IncreasingDecreasingDistanceSet on the first "series" and repeat it

        # 1. We need to create a new IncreasingDecreasingDistanceSet
        seriesSet = IncreasingDecreasingDistanceSet(distance=sum(self.series),
                                                    standardInit = False,
                                                    neutralSegment = self.neutralSegment,
                                                    focusSegment = self.focusSegment)
        
        # 2. We then force the block distances to the values in "series"
        # Note that we need to flip the array as initially an Increase/Decrease set needs to be made on a decreasing distance array
        seriesSet.listBlockDistance = list(np.flip(self.series))
        
        # 3. We then set the "sequence type" by using the native method
        seriesSet.setSequenceType()
        self.sequenceType = seriesSet.sequenceType
        print(seriesSet.sequenceType)

        # 4. We then set the increase or decrease by using the native method
        seriesSet.setIncreaseDecrease()
        print(seriesSet.increaseDecrease)

        # 5. We then create the block of the seriesSet by using the native method too 
        seriesSet.createBlocks()

        # 6. We then store the variation used for seriesSet
        self.variationSegment = seriesSet.variationSegment.copy()

        # 7. We finally create the list of blocks
        Nseries = self.selCombo[3]
        for i in np.arange(Nseries):
            self.listBlock += seriesSet.listBlock