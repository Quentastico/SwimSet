import numpy as np
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

# Make a tool function that allows cutting a set into increasing/decreasing distances
def cutSetStaged(distance, minBlocks):
  # Distance: this is the distance (m) of the set of interest
  # minBlocks: This is the minimal number of blocks allowed in this set
  optionBlocks = []
  for step in np.arange(globals.stepBlockDistance, distance + globals.stepBlockDistance, globals.stepBlockDistance):
    for start in np.arange(globals.minSegmentDistance, distance + globals.stepBlockDistance, globals.stepBlockDistance):

      # Calculating the discrimant (Note that this is always strictly positive)
      delta = (start - step/2)*(start - step/2) + 2*step*distance

      # Calculating the positive solution
      positiveSolution = (step/2-start+np.sqrt(delta))/step

      # Check if the solution is an integer and save the array if there are at least minBlocks segments
      if (positiveSolution == np.floor(positiveSolution)) & (positiveSolution>= minBlocks):
        optionBlocks.append([int(positiveSolution), start, step])

  return optionBlocks

# This utils function defines how the intensity will change from one block of training to the other depending on the pattern selected
def setIntensities(nBlocks, optionIntensity, minIntensity, maxIntensity, selectedIntensity = None):
  # nBlocks: Total number of blocks to consider
  # optionIntensity: can be "intensityIncrease", "intensityDecrease", or "intensityConstant"
  # minIntensity: minimal intensity allowed 
  # maxIntensity: maximal intensity allowed
  # selectedIntensity: selected Intensity (only useful in the case the optionIntensity is "intensityConstant")

  # Create the output, a list of all the intensities selected
  listIntensities = []

  # Case 1: The intensity is constant
  if optionIntensity == "intensityConstant":

    if selectedIntensity is None:
      print("be careful, you are not setting any intensity but asking to have a constant intensity")

    else:
      for i in np.arange(nBlocks):
        listIntensities.append(selectedIntensity)

  # Case 2: The intensity is decreasing/increasing
  else: 

    # Defining the number of intensities possible
    numIntensities = (maxIntensity-minIntensity+1)

    # Case 2.1: The number of possible intensities is higher than the number of blocks: easy, we just find intensities which increase/decrease from one block to another
    if numIntensities >= nBlocks: 

      lowestIntensity = np.random.randint(low=minIntensity, high=maxIntensity-nBlocks+2)

      # Case 2.1.1: Increasing intensity
      if optionIntensity == "intensityIncrease":
        for i in np.arange(nBlocks):
          listIntensities.append(lowestIntensity+i)

      # Case 2.1.2: Decreasing intensity
      if optionIntensity == "intensityDecrease":
        for i in np.arange(nBlocks):
          listIntensities.append(lowestIntensity+nBlocks-1-i)
    
    # Case 2.2: The number of possible intensities is lower than the number of blocks: we have to split them in different schemes
    else: 

      # First we need to find the maximal possible length of a series
      maxWidthIntensity = numIntensities
      while np.floor(nBlocks/maxWidthIntensity) != nBlocks / maxWidthIntensity: 
        maxWidthIntensity -= 1

      # Case 2.2.1: There is a number higher than 1 of options
      if maxWidthIntensity > 1: 

        lowestIntensity = np.random.randint(low=minIntensity, high=maxIntensity-maxWidthIntensity+2)

        # Case 2.2.1.1: Increasing intensity
        if optionIntensity == "intensityIncrease":
          for series in np.arange(np.floor(nBlocks/maxWidthIntensity)):
            for i in np.arange(maxWidthIntensity):
              listIntensities.append(lowestIntensity+i)

        # Case 2.2.1.2: Decreasing intensity
        if optionIntensity == "intensityDecrease":
          for series in np.arange(np.floor(nBlocks/maxWidthIntensity)):
            for i in np.arange(maxWidthIntensity):
              listIntensities.append(lowestIntensity+maxWidthIntensity-1-i)

      # Case 2.2.2: The number of blocks cannot be divided by any other number than 1 (prime number)
      else: 
        # Here we make the choice that we will extend the range of intensities as much as possible even if this means that the block will not be exact
        maxWidthIntensity = numIntensities

        # Case 2.2.2.1: Increasing intensity
        if optionIntensity == "intensityIncrease": 
          nSeries = np.floor(nBlocks/maxWidthIntensity)

          # First adding all the complete series
          for series in np.arange(nSeries):
            for i in np.arange(maxWidthIntensity):
              listIntensities.append(minIntensity+i)

          # Then adding the rest
          for i in np.arange(nBlocks-nSeries*maxWidthIntensity):
            listIntensities.append(int(minIntensity+i))

        # Case 2.2.2.1: Decreasing intensity
        if optionIntensity == "intensityDecrease": 
          nSeries = np.floor(nBlocks/maxWidthIntensity)

          # First adding all the complete series
          for series in np.arange(nSeries):
            for i in np.arange(maxWidthIntensity):
              listIntensities.append(maxIntensity-i)

          # Then adding the rest
          for i in np.arange(nBlocks-nSeries*maxWidthIntensity):
            listIntensities.append(int(maxIntensity-i))

  return listIntensities