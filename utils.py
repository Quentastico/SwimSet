import numpy as np
from itertools import product
import globals

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

# Tool to determine a series of distances which sum is equal to a total distance
def pickDistances(distance, minDistance, avDistance, stepDistance, nDistance):
  # distance: total distance considered 
  # minDistance: the minimal value of any subdistances extracted from the series of distances
  # avDistance: the average subdistance expected
  # stepDIstance: the bigesst common denopmitor of all the distances (e.g. 100m)
  # nDistance: the number of distances to extract 

  listDistance = []

  # First we need to remove the case where nDistance is 1: easy!
  if nDistance==1:
    listDistance.append(int(distance))

  # Then we handle the other cases. 
  else: 

    # Initiatlisation of the "end distance": always keeping enough distance for all the sets
    endDistance = distance - (nDistance-1) * minDistance

    # Then looping on all the distances we want to extract
    for i in np.arange(nDistance-1):

      # Getting the new distance
      newDistance = pickDistance(minValue=minDistance,
                                 maxValue=endDistance,
                                 avValue=avDistance,
                                 stepDistance=stepDistance)
      
      # Storing the new distance
      listDistance.append(int(newDistance))

      # Redefining the end distance
      endDistance += minDistance - newDistance

    # Then adding the last distance
    lastDistance = distance - np.sum(listDistance)
    listDistance.append(int(lastDistance))

  return listDistance
  

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
  for combo in validCombos:
    optionBlock = []
    indexBlockDistance = 0
    for blockDistance in blockDistances:
      for coeff in np.arange(combo[indexBlockDistance]):
        optionBlock.append(int(blockDistance))
      indexBlockDistance += 1
    optionBlocks.append(optionBlock)

  return optionBlocks, scores

# function to find options to split a Frequency Increase set
def splitSetFrequencyIncrease(distance, stepBlockDistance, minBlockDistance, maxBlockDistance, minN, maxN, maxDistanceDiff):

  # 1. first determining all the possible distance values and corresponding combos of n and block distances

  possibleDistances = []
  possibleCombos = []

  for n in np.arange(minN, maxN+1):
    for blockDistance in np.arange(minBlockDistance, maxBlockDistance+stepBlockDistance, stepBlockDistance):

      possibleDistances.append(np.power(n,2) * (n+1) * blockDistance/2)
      possibleCombos.append([n, blockDistance])

  # 2. Calculate the score based on two criteria:
  # Criteria 1: The value of n: the higher, the better
  # Criteria 2: Whether this is the exact value or we have to add 50m rest afterwards. 

  scoreCombos = []

  for i in np.arange(len(possibleCombos)):
    criteria1 = np.power(possibleCombos[i][0], 3)
    if np.floor(possibleDistances[i]/100) == possibleDistances[i]/100:
      criteria2 = 5
    else:
      criteria2 = 0
    scoreCombos.append(criteria1+criteria2)

  # 3. Selecting the possible combos simply based on the distance - Note that we accept a slight difference between the actual and requested distance
  optionCombos = []
  scores = []

  for i in np.arange(len(possibleCombos)):
    if ((distance - possibleDistances[i]) <= maxDistanceDiff) & ((distance - possibleDistances[i])>=0):
      optionCombos.append(possibleCombos[i])
      scores.append(scoreCombos[i])

  return optionCombos, scores

# Function to convert a time expressed in seconds into a time expressed in minutes + seconds
def convertDuration(duration):

  # Minutes
  durationMinutes = int(np.floor(duration/60))

  # Seconds (Note the rounding)
  durationSeconds = int(np.round((duration-60*durationMinutes)/5) * 5)

  return durationMinutes, durationSeconds

# function that removes a type in a given array and also removes the corresponding proba value in an associated array
def removeTypeProba(typeArray, probaArray, typeToRemove):
  
  # typeArray: An array of types (usually of strings)
  # typeProba: An array of probas (normally all between 0 and 1)
  # typeToRemove: A value that is in "typeArray" that needs to be removed

  # Making copies of the arrays
  types = typeArray.copy()
  probas = probaArray.copy()

  # Finding the index of the type to remove
  index = typeArray.index(typeToRemove)

  # Removing the non-wanted values
  types.remove(typeToRemove)
  probas.pop(index)

  # Making sure the sum of probas are still equal to 0
  sumProbas = sum(probas)
  for i in np.arange(len(probas)):
    probas[i] = probas[i]/sumProbas

  return types, probas

# function that determines the type of a set randomly given a distance
def pickSetType(distance):

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
    newSet.setBlockDistance()
    newSetListDistance = newSet.listBlockDistance

    # Redefining the newSetListDistance (for the loop)
    possibleSetTypes, setProba = removeTypeProba(typeArray=possibleSetTypes,
                                                  probaArray=setProba,
                                                  typeToRemove=selSetType)