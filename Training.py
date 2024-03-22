# create a Training object

## IMPORTS

import numpy as np
from utils import pickDistances
import globals
from Set import Set

class Training:

  # Initialisation function
  def __init__(self, distance, standardInit=False):

    # 1. ATTRIBUTE DEFINITION

    self.distance = distance # Total distance of the training session (m)
    self.warmupDistance = None # Warmup distance (m)
    self.cooldownDistance = None # Cooldown distance (m)
    self.mainsetDistance = None # Main Set distance (m)
    self.numberSets = None # Number of sets in the main set
    self.listSetDistance = [] # List of the distances of the sets
    self.listSet = [] # List of sets
    self.standardInit = standardInit
    self.trainingType = None # This indicates what type of training it will be (repeat sets or random)
    self.nSetRepeat = None # IN the case of a repeat set trainig, thi indicates how many sets will repeat at the start of the training

    # 2. DATA CHECKS

    # 2.1. Data Check 1 - Checking that the total distance if higher than the minimal limit
    if self.distance < globals.minTotalDistance:
      print("Please enter a distance value higher than the minimal allowed value: "+ str(globals.minBlockDistance) + "m")
      return

    # 2.2. Data Check 2 - Checking that the distance is a multiple of 100
    if self.distance / 100 != np.floor(self.distance / 100):
      print("Please enter a distance being a multiple of 100m")
      return

    # 3. DISTANCES

    if self.standardInit==True:

      # 3.1. Calculation of the warmup distance
      self.setWarmupDistance()

      # 3.2. Calculation of the cool down distance
      self.setCooldownDistance()

      # 3.3. Calculation of the mainset distance
      self.mainsetDistance = self.distance - self.warmupDistance - self.cooldownDistance

      # 3.4. Determination of the distances of the sets (and number of sets)
      self.setSetDistances()


  # Method to determine the warmup distance
  def setWarmupDistance(self):
    self.warmupDistance = max(globals.minWarmupDistance, 100 * np.round(globals.fracWarmupDistance * self.distance / 100))


  # Method to determine the cooldown distance
  def setCooldownDistance(self):
    self.cooldownDistance = min(100*np.ceil(globals.fracCooldownDistance * self.distance / 100), globals.maxCooldownDistance)

  # Method to determine the split of block distances into the set (and numer of sets too!)
  def setSetDistances(self):

    # 1. Determination of all the possible "combos" of repeat sets + other
    combos = []

    # Looping on all the values of number of repeats (nRepeat) and possible set distances (stepDistance):

    for nRepeat in np.arange(globals.minNumberRepeatSet, globals.maxNumberRepeatSet+1, 1):
      for setDistance in np.arange(globals.minSetDistance, globals.maxRepeatSetDistance+globals.stepSetDistance, globals.stepSetDistance):

        # Defining the distance of the repeat sets (all together) and the remaining distance set
        repeatDistance = nRepeat * setDistance
        remainingDistance = self.mainsetDistance - repeatDistance

        # Selection of the possible cases
        if (remainingDistance == 0) | (remainingDistance >= globals.minSetDistance):

          # Creating the first half of the combo: nRepeat times the distance setDistance
          newCombo = []
          listRepeatDistance = [setDistance] * nRepeat

          # Creating the second part of the combo: the list of the distances

          if remainingDistance > 0:
            nRemainingSet = max(int(np.round(remainingDistance/globals.avSetDistance)), 1)
            listRemainingDistance = pickDistances(distance=remainingDistance,
                                                  minDistance=globals.minSetDistance,
                                                  avDistance=remainingDistance/nRemainingSet,
                                                  stepDistance=globals.stepSetDistance,
                                                  nDistance=nRemainingSet)
          else:
            listRemainingDistance = []

          newCombo = [listRepeatDistance, listRemainingDistance]

          combos.append(newCombo)
    
    # 2. Determination of whether it will be a distanceRepeatSetTraining or a random training
    if len(combos) > 0:
      self.trainingType = np.random.choice(globals.trainingTypes, p=globals.trainingProba)
    else:
      self.trainingType = "Random Training"

    # 3. Then determining the distances and number of sets depending on the type of training
    
    if self.trainingType == "Set Rep Training":
      
      # We first need to choose a random combo
      selComboIndex = np.random.randint(len(combos))
      selCombo = combos[selComboIndex]

      # Then we extract the distances
      self.listSetDistance = selCombo[0] + selCombo[1]
      self.nSetRepeat = len(selCombo[0])
      self.numberSets = len(self.listSetDistance)

    if self.trainingType == "Random Training":

      # We first need to determine the number of sets
      self.numberSets = int(np.round(self.mainsetDistance / globals.avSetDistance))

      # We then use the random pick distance function to determine the set distances
      self.listSetDistance = pickDistances(distance=self.mainsetDistance,
                                           minDistance=globals.minSetDistance,
                                           avDistance=self.mainsetDistance/self.numberSets, # better here to take the actual value of the set rather than the user-defined value
                                           stepDistance=globals.stepSetDistance,
                                           nDistance=self.numberSets)
  
  # Creation of the Sets
  def createSets(self):

    for distance in self.listSetDistance:

      # Extraction of all the possible types of sets
      possibleSetTypes = list(globals.setTypes.keys())
      
      # Initiating the while loop which will make sure that the set can be created
      newSetListDistance = None
      setProba = globals.setProba.copy()

      while newSetListDistance is None:

        # Picking a random set type
        selSetType = np.random.choice(possibleSetTypes, p=setProba)

        # Creating a new set
        newSet = globals.setTypes[selSetType](distance=distance, standardInit=True)

        # Redefining the newSetListDistance
        newSetListDistance = newSet.listBlockDistance

        # Finding the index of the selected set type
        indexSelSetType = possibleSetTypes.index(selSetType)        

        # Removing the possibleSetTypes from the list and redefining the proba
        possibleSetTypes.pop(indexSelSetType)
        setProba.pop(indexSelSetType)
        sumProba = sum(setProba)
        setProba = [setProba[i] / sumProba for i in np.arange(len(setProba))]

      self.listSet.append(newSet)

  # Creating an info method
  def info(self):

    print("SET - Distance: " + str(self.distance))
    print(" WARM UP - Distance: " + str(self.warmupDistance))
    for set in self.listSet:
      set.info()
    print(" COOL DOWN - Distance: " + str(self.cooldownDistance))