import numpy as np
import globals
from itertools import product

# Tool function that picks a random distance between two min and max values
def pickDistance(minValue, maxValue, avValue, stepDistance):
  # minValue (int): Value of the minimal distance of a set (m)
  # maxValue (int): Maximal value allowed for a given set (m)
  # avValue (int): average value for the sets of interest in this training (m)
  # stepDistance(int): should be the acceptable increment of any distance (e.g. if 100m, then possible returned values are 100m, 200m, 300m, etc.)

  # Step 1: Choice of a random value in a normal distribution over the interval
  # [minValue; avValue + avValue - minValue]
  randomValue = np.random.normal(avValue, (avValue - minValue)/3)

  # Step 2: sizing of the random value into the right interval

  # Case 1: The random value is below the minimal value
  if randomValue <= minValue:
    finalValue = minValue
  # Case 2: The random value is between the minimal value and the average value: just rounding the value to the closest stepDistance
  if (randomValue > minValue) & (randomValue <= avValue):
    finalValue = (np.round(randomValue/stepDistance) * stepDistance)
  # Case 3: The random value is beyond the avValue: it needs to be sized to skew the normal distribution
  if (randomValue > avValue) & (randomValue <= maxValue):
    normedValue = avValue + (randomValue-avValue) / (avValue - minValue) * (maxValue-avValue)
    if normedValue > maxValue:
      normedValue = maxValue
    finalValue = np.round(normedValue/stepDistance)*stepDistance
  # Case 4: The random value goes beyond the maximal one
  if randomValue > maxValue:
    finalValue = maxValue

  return finalValue


# Make a tool function that allows cutting a set into increasing/decreasing distances
def splitSetIncreaseDecrease(distance, stepBlockDistance, minBlockDistance, minBlocks):
  # distance: total distance of the set (m)
  # stepBlockDistance: The distance that blocks will increase by withtin the set (m)
  # minBlockDistance: The minimal distance for any block (m)
  # minBlocks: the minimal number of blocks accepted in the set

  optionBlocks = []
  for step in np.arange(stepBlockDistance, distance + stepBlockDistance, stepBlockDistance):
    for start in np.arange(minBlockDistance, distance + stepBlockDistance, stepBlockDistance):

      # Calculating the discrimant (Note that this is always strictly positive)
      delta = (start - step/2)*(start - step/2) + 2*step*distance

      # Calculating the positive solution
      positiveSolution = (step/2-start+np.sqrt(delta))/step

      # Check if the solution is an integer and save the array if there are at least minBlocks segments
      if (positiveSolution == np.floor(positiveSolution)) & (positiveSolution>= minBlocks):
        optionBlocks.append([int(positiveSolution), start, step])

  return optionBlocks

# Make a function that splits a given set with a pyramid pattern
def splitSetPyramid(distance, stepBlockDistance, minBlockDistance, minBlocks): 
  # distance: total distance of the set (m)
  # stepBlockDistance: The distance that blocks will increase by withtin the set (m)
  # minBlockDistance: The minimal distance for any block (m)
  # minBlocks: the minimal number of blocks accepted in the set

  # Looping on all the combination of starting distances and step distances
  optionBlocks = []

  for step in np.arange(stepBlockDistance, distance + stepBlockDistance, stepBlockDistance):
    for start in np.arange(minBlockDistance, distance + stepBlockDistance, stepBlockDistance):

      # Calculating the discrimant (always positive)
      delta = 4*start*start - 4*step*(start-distance)
      
      # Calculating the solution (unique positive solution)
      positiveSolution = (-2*start + np.sqrt(delta)) / (2*step)

      # Check that the solution is a positive integer and that there is the acceptable level of blocks in this set
      if (positiveSolution == np.floor(positiveSolution)) & ( (2*positiveSolution+1) >= minBlocks):
        optionBlocks.append([int(positiveSolution), start, step])
      
  return optionBlocks

# Make a function to split the distance for a DistanceRepSet
def splitSetDistanceRep(distance, stepBlockDistance, minBlockDistance, maxBlockDistance, ratioDistanceRep):

  # 1. First determining the maximal value of the biggest block
  maxBlock = np.min([maxBlockDistance, stepBlockDistance * np.floor(ratioDistanceRep * distance/stepBlockDistance)])

  # 2. Then defining the array of block distances which are possible
  blockDistances = np.arange(minBlockDistance, maxBlock+stepBlockDistance, stepBlockDistance)

  # 3. Defining the maximal value for each coefficient
  maxCoeffs = []
  for blockDistance in blockDistances:
    maxCoeffs.append(np.floor(distance*ratioDistanceRep/blockDistance))

  validCombos = []

  # 4. Selecting the combos which have acceptable values
  nBlockDistances = len(maxCoeffs)

  for combo in product(range(int(np.max(maxCoeffs)+1)), repeat=nBlockDistances):

    # First we make sure that the coeff values do not exceed their max values
    if all(combo[i] <= maxCoeffs[i] for i in range(nBlockDistances)):

      # Then we make sure the sum is equal to the total distance
      sumDistance = np.dot(combo, blockDistances)
      if distance == sumDistance:

        # Then checking that there are not two consecutive zeros
        goodCombo = True
        indexCoeff = 0
        comboCopy = list(combo)

        # First removing the zeros at the start and at the end of the combo
        while comboCopy[0] == 0:
          comboCopy.pop(0)
        while comboCopy[len(comboCopy)-1]==0:
          comboCopy.pop()

        # Then elimitaing the combois with two zeros in a row
        for coeff in comboCopy:
          if (coeff == 0) & (indexCoeff < nBlockDistances-1):
            if comboCopy[indexCoeff+1] == 0:
              goodCombo = False
          indexCoeff += 1

        if goodCombo:
          validCombos.append(combo)

  # Then scoring each combo:
  # Criteria 1 is the number of coefs strictly higher than 1
  # Criteria 2 is the number of different block distances
  scores = []
  for combo in validCombos:
    criteria1 = np.sum([combo[i] > 1 for i in range(nBlockDistances)])
    criteria2 = np.sum([combo[i] > 0 for i in range(nBlockDistances)])
    criteria = criteria1 + criteria2/(nBlockDistances+1)
    scores.append(np.power(criteria,3))

  # Finally converting the validCombos (only ranges of coefficients) into blocks
  optionBlocks = []
  indexBlockDistance = 0
  for combo in validCombos:
    for blockDistance in blockDistances:
      for coeff in np.arange(combo[indexBlockDistance]):
        optionBlocks.append(int(blockDistance))
      indexBlockDistance += 1

  return optionBlocks, scores