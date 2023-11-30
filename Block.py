import numpy as np
import globals

class Block:

  # Initialisation function
  def __init__(self, distance, randomDef = True, listSegment = [], listSegmentDistance = []):

    # Attributes
    self.distance = distance # Block distance (in m)
    self.randomDef = randomDef # If true, then we define a complete random Block; otherwise, some elements are user-defined.
    self.breakDuration = None # Duration of the break after each block (in s)
    self.duration = None # Duration of the entire block (in s)
    self.listSegment = listSegment # List that contains all the segment composing the block
    self.listSegmentDistance = listSegmentDistance # List that contains the distance of the Segments composing the Block

    if self.randomDef:

      # Definition of the list of the Segments composing the Block
      self.listSegmentDistance = []
      self.setDistanceSegments()

      # Creation of the list of the Segments attached to this object
      self.listSegment = []
      for segmentDistance in self.listSegmentDistance:
        print(segmentDistance)
        newSegment = Segment(distance=segmentDistance, randomDef=True)
        self.listSegment.append(newSegment)


  # Definition of the function that splits the block distance into segments
  def setDistanceSegments(self):

    # Determining the number of segments randomly between the minimum and maximum numbers
    numberSegments = np.random.randint(low=minSegmentNumber, high=maxSegmentNumber+1)

    # Checking that the number of segments are compatible with the distance
    if self.distance/numberSegments < minSegmentDistance:
      numberSegments = int(np.floor(self.distance/minSegmentDistance))

    # Attributing random values within the block

    if numberSegments == 1:
      self.listSegmentDistance.append(self.distance)

    else:

      #Initialise the loop by setting the min and max values
      minValue = minSegmentDistance
      avValue = self.distance / numberSegments

      for i in np.arange(numberSegments-1):

        # Setting the max Distance
        maxValue = self.distance - np.array(self.listSegmentDistance).sum() - (numberSegments - 1 - i) * minSegmentDistance

        # Picking a random distance in the given interval and add it to the list
        newDistanceValue = pickDistance(minValue, maxValue, avValue, minSegmentDistance)
        self.listSegmentDistance.append(int(newDistanceValue))

      # At the end of the loop (or if there is only one set), the last set is defined
      self.listSegmentDistance.append(int(self.distance - np.array(self.listSegmentDistance).sum()))