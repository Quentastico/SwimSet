## IMPORTS
import numpy as np
import globals
from utils import splitSetDistanceRep
from Block import Block
from Set import Set
import utils

class DistanceRepSet(Set):

    # Object initialisation
    def __init__(self, distance, standardInit=False):

        super().__init__(distance, standardInit=standardInit)

        self.type = "Distance Rep"

        if self.standardInit:
            self.setBlockDistances()
            self.createBlocks()

    # Method to split the set into a given distance
    def setBlockDistances(self): 

        # Making sure that the distance is lower than 800m (to avoid very long calculation times)
        if self.distance > 800:
            print("Careful - The DistanceRep type of set is not catered for distances beyond 800m")
            self.listBlockDistance = None

        else:

            # 1. Get all the possible combinations
            optionBlocks, scores = splitSetDistanceRep(distance=self.distance,
                                                       stepBlockDistance=globals.stepBlockDistance,
                                                       minBlockDistance=globals.minBlockDistance,
                                                       maxBlockDistance=globals.maxBlockDistance,
                                                       ratioDistanceRep=globals.ratioDistanceRep)
            
            #2. Then picking a combination based on the scores
            probaCombo = scores/sum(scores)
            selOptionIndex = np.random.choice(np.arange(len(optionBlocks)), p=probaCombo)
            self.listBlockDistance = optionBlocks[selOptionIndex]




        
