# IMPORTS

import numpy as np
import globals

# Making a tool to split a given set in blocks of increasing reps/ decreasing the distance
def splitSetDistanceRep(distance): 

  optionCombos = []

  # Here we make a three-loop that will calculate all possible combos of reps, steps and starting points
  for n in np.arange(2, np.floor((distance+globals.minBlockDistance)/globals.minBlockDistance), 1): 
    for start in np.arange(globals.minBlockDistance, distance+globals.stepBlockDistance, globals.stepBlockDistance):
      for step in np.arange(globals.stepBlockDistance, distance+globals.stepBlockDistance, globals.stepBlockDistance):

        # Calculation of the sum of the squares from 1 to n-1
        sum_squares = 0
        for i in np.arange(n): 
          sum_squares += np.square(i)

        # Calculation of the complete formula
        result = np.square(n)*start + n/2*(n-1)*(n*step-start) - step*sum_squares

        # Check if the sum is equal to the total distance; if yes, we keep the combo
        if result == distance:
          optionCombos.append([n, start, step])

  # Then we have to select the best possible sets, based on the following criteria: 
  # - Case 1: If there is a combo with at least n>=3, then we only keep combos with n>=3 (more fun)
  # - Case 2: if it is not the case, then we keep only one option: the combo with n=2 which ensure miminal difference between start and step
  # - if really there is nothing, the distance we spit out is the distance

  # Let's first then elimiate the Case 3
  if len(optionCombos) == 0:

    print("we tried a distanceRep for this set but it did not work - this set will be boring as")
    optionBlocks = [distance]

  else:

    optionBlocks = []

    # First we calculate the highest value of n
    maxN = 2
    for combo in optionCombos:
      if combo[0] > maxN:
        maxN = combo[0]
    
    # Then we split in the two different cases

    # Case 1: There is at least one combo with at least n>=3
    if maxN >=3: 
      for combo in optionCombos:
        if combo[0]>=3:
          newBlock = unwrapDistanceRepCombo(combo)
          optionBlocks.append(newBlock)
    
    # Case 2: There is not
    else: 
      diff = 100000

      for combo in optionCombos:
        newDiff = np.abs(combo[1]-combo[2])
        if newDiff < diff: 
          selCombo = combo
          diff = newDiff

      newBlock = unwrapDistanceRepCombo(selCombo) 
      optionBlocks.append(newBlock)

    return optionBlocks


# This function "unwraps" a combo composed of n, start and step in the case where the distance of blocks withtin a set follow a "Distance Rep" pattern
def unwrapDistanceRepCombo(combo): 

  n = combo[0]
  start = combo[1]
  step = combo[2]

  optionBlocks = []

  for i in np.arange(1, n+1): 
    for p in np.arange(i):
      optionBlocks.append(start + (n-i)*step)

  return optionBlocks

