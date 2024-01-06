# create a Training object

## IMPORTS

import numpy as np
from utils import pickDistance
import globals
from Set import Set

class Training:

  # Initialisation function
  def __init__(self, distance, numberSets = None):

    # 1. ATTRIBUTE DEFINITION

    self.distance = distance # Total distance of the training session (m)
    self.warmupDistance = None # Warmup distance (m)
    self.cooldownDistance = None # Cooldown distance (m)
    self.mainsetDistance = None # Main Set distance (m)
    self.numberSets = numberSets # Number of sets in the main set (can be user-defined)
    self.listSetDistance = [] # List of the distances of the sets
    self.listSet = [] # List of sets

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

    # 3.1. Calculation of the warmup distance
    self.setWarmupDistance()

    # 3.2. Calculation of the cool down distance
    self.setCooldownDistance()

    # 3.3. Calculation of the mainset distance
    self.mainsetDistance = self.distance - self.warmupDistance - self.cooldownDistance

    # 3.4. Determination of the number of sets
    self.setNumberSets()

    # 3.5. Determination of the distances of the sets
    self.setSetDistances()

    # 4. CREATION OF THE SETS

    # 4.1. Creation of the Sets
    self.createSets()


  # Method to determine the warmup distance
  def setWarmupDistance(self):
    self.warmupDistance = max(globals.minWarmupDistance, 100 * np.round(globals.fracWarmupDistance * self.distance / 100))


  # Method to determine the cooldown distance
  def setCooldownDistance(self):
    self.cooldownDistance = min(100*np.ceil(globals.fracCooldownDistance * self.distance / 100), globals.maxCooldownDistance)


  # Method to determine the right number of sets
  def setNumberSets(self):

    # Case 1 - The user has entered a valid value: we want to make sure that on average, the minimum set distance is higher than the minimal value allowed
    if self.numberSets is not None:
      if self.mainsetDistance / self.numberSets < globals.minSetDistance:
        print("Careful: the number of sets is too high for the selected distance")
        # In this case, we set the number of sets so that the distance per set is equal to the minimal allowed value
        self.numberSets = int(np.floor(self.mainsetDistance / globals.minSetDistance))

    # Case 2: The user has entered no value
    else:
      self.numberSets = int(np.round(self.mainsetDistance / globals.avSetDistance))

  # Method to determine the list of the lengths of the sets
  def setSetDistances(self):

    if self.numberSets > 1:

      #Initialise the loop by setting the min and max values
      minValue = globals.minSetDistance
      avValue = self.mainsetDistance / self.numberSets

      for i in np.arange(self.numberSets-1):

        # Setting the max Distance
        maxValue = self.mainsetDistance - np.array(self.listSetDistance).sum() - (self.numberSets - 1 - i) * globals.minSetDistance

        # Picking a random distance in the given interval and add it to the list
        newDistanceValue = pickDistance(minValue, maxValue, avValue, 100)
        self.listSetDistance.append(int(newDistanceValue))

    # At the end of the loop (or if there is only one set), the last set is defined
    self.listSetDistance.append(int(self.mainsetDistance - np.array(self.listSetDistance).sum()))
  
  # Creation of the Sets
  def createSets(self):

    for distance in self.listSetDistance:
      newSet = Set(distance=distance)
      self.listSet.append(newSet)

  # Creating an info method
  def info(self):

    print("SET - Distance: " + str(self.distance))
    print(" WARM UP - Distance: " + str(self.warmupDistance))
    for set in self.listSet:
      set.info()
    print(" COOL DOWN - Distance: " + str(self.cooldownDistance))