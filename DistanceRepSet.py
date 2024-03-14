## IMPORTS
import numpy as np
import globals
from utils import splitSetDistanceRep
from Block import Block
from Set import Set
from Variation import Variation
import utils

class DistanceRepSet(Set):

    # Object initialisation
    def __init__(self, distance, standardInit=False):

        super().__init__(distance, standardInit=standardInit)

        self.type = "Distance Rep"
        self.increaseDecrease = "" # This attribute will determine if the set will have blocks increasing or decreasing in length

        if self.standardInit:
            self.setBlockDistances()
            self.setIncreaseDecrease()
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

    # Method to decide if this will be a decrease or an increase
    def setIncreaseDecrease(self):
        
        self.increaseDecrease = np.random.choice(globals.increaseDecreaseType, p=globals.increaseDecreaseProba)

    # Method to create blocks
    def createBlocks(self):

        # 1. Create an initial block - only one segment
        firstBlock = Block(distance=self.listBlockDistance[0], nSegments=1)
        firstBlock.setSegmentDistances()
        firstBlock.createSegments()

        # 2. Then repeat the block and only change the distance of the block
        for distance in self.listBlockDistance:
            newBlock = firstBlock.copy()
            newBlock.distance = distance
            newBlock.listSegmentDistance = [distance]
            newBlock.listSegment[0].distance = distance
            self.listBlock.append(newBlock)

        # 3. Then determine what parameter can change from one block to the other
        varyingParameters = firstBlock.listSegment[0].getVaryingParameters()

        # 4. Then creating a variation
        variationSegment =  Variation(allowedVariation=globals.allowedVariationDistanceRep1,
                                      varyingParameters=varyingParameters,
                                      nBlocks = len(self.listBlockDistance),
                                      standardInit=True)
        self.variationSegment = variationSegment

        # 5. Then changing the value of the changing parameter from one block to the other
        if variationSegment.selParameter is not None: 
            indexBlock = 0
            for block in self.listBlock:
                block.listSegment[0].setForcedParameter(parameterName=variationSegment.selParameter, 
                                                        parameterValue=variationSegment.selParameterVariation[indexBlock])
                indexBlock += 1

        # 6. Finally flipping the block if necessary
        if self.increaseDecrease == "decrease":
            self.listBlockDistance = np.flip(self.listBlockDistance)
            self.listBlock = np.flip(self.listBlock)
    




        
