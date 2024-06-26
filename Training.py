# create a Training object

## IMPORTS

import numpy as np
from utils import pickDistances
from utils import removeTypeProba
from Set import Set
from MetaSet import MetaSet
from ConstantDistanceSet import ConstantDistanceSet
from IncreasingDecreasingDistanceSet import IncreasingDecreasingDistanceSet
from PyramidDistanceSet import PyramidDistanceSet
from DistanceRepSet import DistanceRepSet
from FrequencyIncreaseSet import FrequencyIncreaseSet
from CyclicDistanceSet import CyclicDistanceSet
import settings

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
    # Useful dictionary which will associate a settype to its name
    self.setTypes =  {"Constant Distance": ConstantDistanceSet,
                      "Increasing/Decreasing Distance": IncreasingDecreasingDistanceSet, 
                      "Pyramid Distance": PyramidDistanceSet,
                      "Distance Rep": DistanceRepSet,
                      "Frequency Increase": FrequencyIncreaseSet,
                      "Cyclic Distance": CyclicDistanceSet}
    self.metaSet = None #This will contain the metaSet object if it is calculated. 

    # 2. DATA CHECKS

    # 2.1. Data Check 1 - Checking that the total distance if higher than the minimal limit
    if (self.distance < settings.globals.minTotalDistance):
      if self.verbose >= 1: 
        print("Please enter a distance value higher than the minimal allowed value: "+ str(settings.globals.minBlockDistance) + "m")
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

    self.warmupDistance = int(max(settings.globals.minWarmupDistance, 100 * np.round(settings.globals.fracWarmupDistance * self.distance / 100)))


  # Method to determine the cooldown distance
  def setCooldownDistance(self):

    self.cooldownDistance = int(min(100*np.ceil(settings.globals.fracCooldownDistance * self.distance / 100), settings.globals.maxCooldownDistance))

  # Method to determine the split of block distances into the set (and numer of sets too!)
  def setSetDistances(self):

    # 1. Determination of the maximal number of repeats of the same set

    # We first start with "6" repeats, which is not possible 
    maxRepeatSet = settings.globals.maxNumberRepeatSet + 1
    repeatPossible = False

    # Then we loop on max repeat by removing one at each time of the loop
    while (~repeatPossible) & (maxRepeatSet > settings.globals.minNumberRepeatSet):
      maxRepeatSet -= 1
      metaSet = MetaSet(numberSets=maxRepeatSet, standardInit=True)
      if len(metaSet.listFocusSegments) > 0:
        repeatPossible = True

    # 1. Determination of all the possible "combos" of repeat sets + other
    combos = []

    # Looping on all the values of number of repeats (nRepeat) and possible set distances (stepDistance):
    # Note that we only do this when there is a potential metaSet available

    if repeatPossible: 

      for nRepeat in np.arange(settings.globals.minNumberRepeatSet, maxRepeatSet+1, 1):
        for setDistance in np.arange(settings.globals.minSetDistance, settings.globals.maxRepeatSetDistance+settings.globals.stepSetDistance, settings.globals.stepSetDistance):

          # Defining the distance of the repeat sets (all together) and the remaining distance set
          repeatDistance = nRepeat * setDistance
          remainingDistance = self.mainsetDistance - repeatDistance

          # Selection of the possible cases
          if (remainingDistance == 0) | (remainingDistance >= settings.globals.minSetDistance):

            # Creating the first half of the combo: nRepeat times the distance setDistance
            newCombo = []
            listRepeatDistance = [setDistance] * nRepeat

            # Creating the second part of the combo: the list of the distances

            if remainingDistance > 0:
              nRemainingSet = max(int(np.round(remainingDistance/settings.globals.avSetDistance)), 1)
              listRemainingDistance = pickDistances(distance=remainingDistance,
                                                    minDistance=settings.globals.minSetDistance,
                                                    avDistance=remainingDistance/nRemainingSet,
                                                    stepDistance=settings.globals.stepSetDistance,
                                                    nDistance=nRemainingSet)
            else:
              listRemainingDistance = []

            newCombo = [listRepeatDistance, listRemainingDistance]

            combos.append(newCombo)
    
    # 2. Determination of whether it will be a distanceRepeatSetTraining or a random training
    if len(combos) > 0:
      self.trainingType = np.random.choice(settings.globals.trainingTypes, p=settings.globals.trainingProba)
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
      self.numberSets = np.max([1, int(np.round(self.mainsetDistance / settings.globals.avSetDistance))])

      # We then use the random pick distance function to determine the set distances
      self.listSetDistance = pickDistances(distance=self.mainsetDistance,
                                           minDistance=settings.globals.minSetDistance,
                                           avDistance=self.mainsetDistance/self.numberSets, # better here to take the actual value of the set rather than the user-defined value
                                           stepDistance=settings.globals.stepSetDistance,
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
      self.metaSet = metaSet

      # 4. Then we create the first set of the series
      if self.verbose >=2:
        print("SET 1 creation")
        print("Set type: " + selSetType)

      firstSet = self.setTypes[selSetType](distance=listRepeatDistance[0],
                                              standardInit=True,
                                              neutralSegment=metaSet.listNeutralSegments[0],
                                              focusSegment=metaSet.listFocusSegments[0], 
                                              verbose=self.verbose)
      self.listSet.append(firstSet)     
      
      # 5. Then we create the following sets by copying the first set using the newFocusCopy() method of set
      if len(listRepeatDistance) > 1:
        for i in np.arange(len(listRepeatDistance)-1):
          if self.verbose >= 2:
            print("SET " + str(i+2) + " Creation")
            print("Set type: " + selSetType)
          newSet = firstSet.newFocusCopy(newFocusSegment=metaSet.listFocusSegments[i+1], 
                                         newNeutralSegment=metaSet.listNeutralSegments[i+1])
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
        newSet = self.setTypes[selSetType](distance=distance, standardInit=True, verbose=self.verbose)
        self.listSet.append(newSet)        

    if self.trainingType == "Random Training": # Random Training

      for distance in self.listSetDistance:
          
        # 1. First select the type of the set
        selSetType = self.pickSetType(distance=distance)

        if self.verbose >= 2:
          print("NEW SET Creation")
          print("Set type: " + selSetType)

        # 2. Then create the set and add it to the list
        newSet = self.setTypes[selSetType](distance=distance, standardInit=True, verbose=self.verbose)
        self.listSet.append(newSet)


  # Defining a util function to pick a set type
  def pickSetType(self, distance):

    # distance: the distance of the set (m)
          
    # Extraction of all the possible types of sets
    possibleSetTypes = settings.globals.setTypes.copy()
          
    # Initiating the while loop which will make sure that the set can be created
    newSetListDistance = []
    setProba = settings.globals.setProba.copy()

    while len(newSetListDistance) == 0:

      # Picking a random set type
      selSetType = np.random.choice(possibleSetTypes, p=setProba)

      # Creating a new set
      newSet = self.setTypes[selSetType](distance=distance, standardInit=False, verbose=self.verbose)
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

  # Creation of the dictionary output for the API
  def dictionary(self):

    listSetDictionary = []
    for set in self.listSet:
      listSetDictionary.append(set.dictionary())

    trainingDictionary = {"trainingType": self.trainingType,
                          "warmupDistance": int(self.warmupDistance),
                          "cooldownDistance": int(self.cooldownDistance),
                          "trainingDistance": int(self.distance),
                          "listSet": listSetDictionary}
    
    return trainingDictionary

  ## Creating a method that computes the average time per 100m (mainly for testing purposes)
  def calcAvPace(self):

    totalDuration = 0
    for qSet in self.listSet:
      for block in qSet.listBlock:
        for segment in block.listSegment:
          totalDuration += segment.duration

    return totalDuration / self.mainsetDistance * 100

  ## Creating now a method that computes the percenatges of the main set in each stroke
  def calcAvStrokes(self):

    strokePercentages = {}

    # Initialisation of a cumulated distance of 0 in the dictionary for each stroke
    for stroke in settings.globals.strokeTypes:
      strokePercentages[stroke] = 0

    # Then counting the distance for each stroke in each segment
    for qSet in self.listSet:
      for block in qSet.listBlock:
        for segment in block.listSegment:
          strokePercentages[segment.stroke] += segment.distance
    
    # Then calculating these as ratio of the distance in the main set
    for stroke in settings.globals.strokeTypes:
      strokePercentages[stroke] = np.round(strokePercentages[stroke] / self.mainsetDistance * 100)

    return strokePercentages
  
  ## Creates a method that computes the percentages of the main set with each type of equipment
  def calcAvEquipment(self):

    equipmentPercentages = {}

    # Initialisation of a cumulated distance of 0 for each equipment
    for equipment in settings.globals.equipmentTypes:
      equipmentPercentages[equipment] = 0

    # Then adding the distance for each equipment for each segment
    for qSet in self.listSet:
      for block in qSet.listBlock:
        for segment in block.listSegment:
          equipmentPercentages[segment.equipment] += segment.distance

    # Then calculating percentages of main set distance
    for equipment in settings.globals.equipmentTypes:
      equipmentPercentages[equipment] = np.round(equipmentPercentages[equipment] / self.mainsetDistance * 100)

    return equipmentPercentages
  
  ## Creates a method to calculate the frequency of drill
  def calcAvDrill(self): 

    drillPercentage = 0

    ## Adding the distance of drills from each segment
    for qSet in self.listSet:
      for block in qSet.listBlock:
        for segment in block.listSegment:
          if "drill " in segment.drill: 
            drillPercentage += segment.distance

    ## Calculating the percenatge
    drillPercentage = np.round(drillPercentage / self.mainsetDistance * 100)

    return drillPercentage
  
  ## Creation of a method to calculate the total kick distance in the main set
  def calcAvKick(self):

    kickPercentage = 0

    ## Adding the distances of kick segment by segment
    for qSet in self.listSet:
      for block in qSet.listBlock:
        for segment in block.listSegment:
          if segment.kick == "kick": 
            kickPercentage += segment.distance

    # Calculating the percentage
    kickPercentage = np.round(kickPercentage/self.mainsetDistance * 100)

    return kickPercentage