import numpy as np
import globals
from utils import pickDistance
from Segment import Segment


class Block:

  # Initialisation function
  def __init__(self, distance, nSegments = None):

    # Attributes
    self.distance = distance # Block distance (in m)
    self.breakDuration = None # Duration of the break after each block (in s)
    self.duration = None # Duration of the entire block (in s)
    self.listSegment = [] # List that contains all the segment composing the block
    self.listSegmentDistance = [] # List that contains the distance of the Segments composing the Block
    self.nSegments = nSegments # Number of segments in the block (can be user-defined)

    # Definition of the list of the Segments composing the Block
    self.setDistanceSegments()

    # Creation of the list of the Segments attached to this object
    self.listSegment = []
    for segmentDistance in self.listSegmentDistance:
      newSegment = Segment(distance=segmentDistance, randomDef=True)
      self.listSegment.append(newSegment)

  # Making a function to provide info on a block
  def info(self):

    print("   BLOCK: Distance: " + str(self.distance) + ", List of segment distances: " + str(self.listSegmentDistance))
    for segment in self.listSegment:
      segment.info()


  # Making a function that copies an existing block

  def copy(self):

    # Initialising the object
    newBlock = Block(distance = self.distance)

    # Copying the properties
    newBlock.randomDef = self.randomDef
    newBlock.breakDuration = self.breakDuration
    newBlock.duration = self.duration
    newBlock.listSegmentDistance = self.listSegmentDistance
    newBlock.nSegments = self.nSegments

    # Copying the list of segments - This needs to be performed Segment after Segment
    newBlock.listSegment = []

    for segment in self.listSegment:
      newSegment = segment.copy()
      newBlock.listSegment.append(newSegment)

    # returning the new object
    return newBlock



  # Definition of the function that splits the block distance into segments
  def setDistanceSegments(self):

    # Determining the number of segments randomly between the minimum and maximum numbers (if not already user-defined)
    if self.nSegments is None:  

      self.nSegments = np.random.randint(low=globals.minSegmentNumber, high=globals.maxSegmentNumber+1)

      # Checking that the number of segments are compatible with the distance
      if self.distance/self.nSegments < globals.minSegmentDistance:
        self.nSegments = int(np.floor(self.distance/globals.minSegmentDistance))

    # Attributing random values within the block

    if self.nSegments == 1:
      self.listSegmentDistance.append(self.distance)

    else:

      #Initialise the loop by setting the min and max values
      minValue = globals.minSegmentDistance
      avValue = self.distance / self.nSegments

      for i in np.arange(self.nSegments-1):

        # Setting the max Distance
        maxValue = self.distance - np.array(self.listSegmentDistance).sum() - (self.nSegments - 1 - i) * globals.minSegmentDistance

        # Picking a random distance in the given interval and add it to the list
        newDistanceValue = pickDistance(minValue, maxValue, avValue, globals.minSegmentDistance)
        self.listSegmentDistance.append(int(newDistanceValue))

      # At the end of the loop (or if there is only one set), the last set is defined
      self.listSegmentDistance.append(int(self.distance - np.array(self.listSegmentDistance).sum()))