# create a Training object

## IMPORTS

import numpy as np
from utils import pickDistances
from utils import removeTypeProba
import globals
from Set import Set
from MetaSet import MetaSet

class Training:

  # Initialisation function
  def __init__(self, distance, standardInit=False, verbose=0):

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
    self.combo = [] # In the case of a repeat set training, this is the combo defining the distances
    self.verbose = verbose # defines the level of information displayed to to the user (0: no info; increases with this argument)

    # 2. DATA CHECKS

    # 2.1. Data Check 1 - Checking that the total distance if higher than the minimal limit
    if (self.distance < globals.minTotalDistance):
      if self.verbose >= 1: 
        print("Please enter a distance value higher than the minimal allowed value: "+ str(globals.minBlockDistance) + "m")
      return

    # 2.2. Data Check 2 - Checking that the distance is a multiple of 100
    if self.distance / 100 != np.floor(self.distance / 100):
      if self.verbose >= 1:
        print("Please enter a distance being a multiple of 100m")
      return

    # 3. DISTANCES

    if self.standardInit==True:

      # 3.1. Calculation of the warmup distance
      self.setWarmupDistance()
      if self.verbose >= 2:
        print("Warm up distance calculated")

      # 3.2. Calculation of the cool down distance
      self.setCooldownDistance()
      if self.verbose >= 2:
        print("Cooldown distance calculated")

      # 3.3. Calculation of the mainset distance
      self.mainsetDistance = self.distance - self.warmupDistance - self.cooldownDistance
      if self.verbose >= 2:
        print("Main set distance calculated")

      # 3.4. Determination of the distances of the sets (and number of sets)
      self.setSetDistances()
      if self.verbose >= 2:
        print("Set distance calculated")
        print("Distance of the sets:") 
        print(self.listSetDistance)
        print("Training Type")
        print(self.trainingType)

      # 3.5. Creation of the sets
      self.createSets()


  # Method to determine the warmup distance
  def setWarmupDistance(self):

    self.warmupDistance = max(globals.minWarmupDistance, 100 * np.round(globals.fracWarmupDistance * self.distance / 100))


  # Method to determine the cooldown distance
  def setCooldownDistance(self):

    self.cooldownDistance = min(100*np.ceil(globals.fracCooldownDistance * self.distance / 100), globals.maxCooldownDistance)

  # Method to determine the split of block distances into the set (and numer of sets too!)
  def setSetDistances(self):

    # 1. Determination of the maximal number of repeats of the same set

    # We first start with "6" repeats, which is not possible 
    maxRepeatSet = globals.maxNumberRepeatSet + 1
    repeatPossible = False

    # Then we loop on max repeat by removing one at each time of the loop
    while (~repeatPossible) & (maxRepeatSet > globals.minNumberRepeatSet):
      maxRepeatSet -= 1
      metaSet = MetaSet(numberSets=maxRepeatSet, standardInit=True)
      if len(metaSet.listFocusSegments) > 0:
        repeatPossible = True

    # 1. Determination of all the possible "combos" of repeat sets + other
    combos = []

    # Looping on all the values of number of repeats (nRepeat) and possible set distances (stepDistance):
    # Note that we only do this when there is a potential metaSet available

    if repeatPossible: 

      for nRepeat in np.arange(globals.minNumberRepeatSet, maxRepeatSet+1, 1):
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
      self.combo = selCombo.copy()

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

    # Here we have two ways to create the sets
    # If we are in a distance Set format, then we need to repeat the same type of set logically
    # with some changes according to a pattern (this is what metaSet is for)
    # But if we are not in a meta set, then we need to be more random.

    if self.trainingType == "Set Rep Training": #Meta set

      # 1. We first create the repeating sets
      listRepeatDistance = self.combo[0]

      # 2. We then determine randomly the set type for this repeat set
      selSetType = self.pickSetType(distance=listRepeatDistance[0])

      # 3. Making the meta Set that will determine the pattern to follow in these first sets
      metaSet = MetaSet(numberSets=len(listRepeatDistance), standardInit=True)

      # 4. Then we create the first set of the series
      if self.verbose >=2:
        print("SET 1 creation")
        print("Set type: " + selSetType)

      firstSet = globals.setTypes[selSetType](distance=listRepeatDistance[0],
                                              standardInit=True,
                                              neutralSegment=metaSet.neutralSegment,
                                              focusSegment=metaSet.listFocusSegments[0])
      self.listSet.append(firstSet)

      
      
      # 5. Then we create the following sets by copying the first set using the newFocusCopy() method of set
      if len(listRepeatDistance) > 1:
        for i in np.arange(len(listRepeatDistance)-1):
          if self.verbose >= 2:
            print("SET " + str(i+2) + " Creation")
            print("Set type: " + selSetType)
          newSet = firstSet.newFocusCopy(newFocusSegment=metaSet.listFocusSegments[i+1])
          self.listSet.append(newSet)
          

      # 5. then for the remaining sets, we just create random sets each time
      listNonRepeatDistance = self.combo[1]

      for distance in listNonRepeatDistance:

        # First select the type of the set
        selSetType = self.pickSetType(distance=distance)

        if self.verbose >= 2:
            print("NEW SET Creation")
            print("Set type: " + selSetType)

        # Then create the set and add it to the list
        newSet = globals.setTypes[selSetType](distance=distance, standardInit=True)
        self.listSet.append(newSet)        

    if self.trainingType == "Random Training": # Random Training

      for distance in self.listSetDistance:
          
        # 1. First select the type of the set
        selSetType = self.pickSetType(distance=distance)

        if self.verbose >= 2:
          print("NEW SET Creation")
          print("Set type: " + selSetType)

        # 2. Then create the set and add it to the list
        newSet = globals.setTypes[selSetType](distance=distance, standardInit=True)
        self.listSet.append(newSet)


  # Defining a util function to pick a set type
  def pickSetType(self, distance):

    # distance: the distance of the set (m)
          
    # Extraction of all the possible types of sets
    possibleSetTypes = list(globals.setTypes.keys())
          
    # Initiating the while loop which will make sure that the set can be created
    newSetListDistance = None
    setProba = globals.setProba.copy()

    while newSetListDistance is None:

      # Picking a random set type
      selSetType = np.random.choice(possibleSetTypes, p=setProba)

      # Creating a new set
      newSet = globals.setTypes[selSetType](distance=distance, standardInit=False)
      newSet.setBlockDistances()
      newSetListDistance = newSet.listBlockDistance

      # Redefining the newSetListDistance (for the loop)
      possibleSetTypes, setProba = removeTypeProba(typeArray=possibleSetTypes,
                                                    probaArray=setProba,
                                                    typeToRemove=selSetType)
    
    return selSetType

  # Creating an info method
  def info(self):

    print("SET - Distance: " + str(self.distance))
    print(" WARM UP - Distance: " + str(self.warmupDistance))
    for set in self.listSet:
      set.info()
    print(" COOL DOWN - Distance: " + str(self.cooldownDistance))