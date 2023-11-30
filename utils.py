import numpy as np

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