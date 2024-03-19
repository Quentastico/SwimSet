## GLOBAL VARIABLES

import numpy as np
import globals
from Block import Block
from utils import convertDuration

class Set:

  # Initialisation function
  def __init__(self, distance, standardInit=False):

    # 1. ATTRIBUTES

    self.distance = distance # Distance of the set (m)
    self.standardInit = standardInit # This indicates if the set will be defined automatically during the init or not
    self.type = None # Type of variation of distances for the different blocks composing the Set
    self.listBlockDistance = [] # List of the distances of the block composing the set (in m)
    self.listBlock = [] # List of the block objects that will compose the Set
    self.variationSegment = None # The variation object that describes the variation selected for the set. 
    self.sequenceType = "" # This will indicate what type of sequence this set is: "Half-half", "buildblock", etc. 
    self.duration = None # This will contain the duration of the set in seconds

  # Method to finalise a block by fixing any issue with the segments withtin the set and calculating the duration of the segments, blocks and segments. 
  def finalise(self):

    # Initialisasing the duration of the set
    self.duration =0

    # Looping on all the blocks withtin the set
    for block in self.listBlock:
      block.finalise()
      self.duration += block.duration

  # Info method        
  def info(self):

    # distance
    printDistance = "Distance: " + str(self.distance)

    # Type of set
    printType = " Type: " + self.type + " " + self.sequenceType

    # Duration
    if self.duration is not None: 
      durationMinutes, durationSeconds = convertDuration(self.duration)
      printDuration = " - " + str(durationMinutes) + "min" + str(durationSeconds) + "s"

    print("  SET - " + printDistance + printType + printDuration)
    for block in self.listBlock:
      block.info()
