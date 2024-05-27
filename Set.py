## GLOBAL VARIABLES

import numpy as np
from Block import Block
from utils import convertDuration
import settings

class Set:

  # Initialisation function
  def __init__(self, distance, standardInit=False, neutralSegment=None, focusSegment=None):

    # 1. ATTRIBUTES

    self.distance = distance # Distance of the set (m)
    self.standardInit = standardInit # This indicates if the set will be defined automatically during the init or not
    self.neutralSegment = neutralSegment # This attribute will contain the value of the "neutral segment" in the case of a metaset
    self.focusSegment = focusSegment # This attribute will contain the value of the "focus segment"
    self.type = None # Type of variation of distances for the different blocks composing the Set
    self.listBlockDistance = [] # List of the distances of the block composing the set (in m)
    self.listBlock = [] # List of the block objects that will compose the Set
    self.variationSegment = None # The variation object that describes the variation selected for the set. 
    self.sequenceType = "" # This will indicate what type of sequence this set is: "Half-half", "buildblock", etc. 
    self.duration = None # This will contain the duration of the set in seconds

  # Method to finalise a block by fixing any issue with the segments withtin the set and calculating the duration of the segments, blocks and segments. 
  def finalise(self):

    # Initialisasing the duration of the set
    self.duration = 0

    # Looping on all the blocks withtin the set
    for block in self.listBlock:
      block.finalise()
      self.duration += block.duration

  # Copy method
  def copy(self):

    # Creating a new empty set
    newSet = Set(distance=self.distance)
    
    # Copying all the attribute values of the set - With the exception of the list of blocks
    newSet.standardInit = self.standardInit # This indicates if the set will be defined automatically during the init or not
    if self.neutralSegment is not None:
      newSet.neutralSegment = self.neutralSegment.copy() # This attribute will contain the value of the "neutral segment" in the case of a metaset
    if self.focusSegment is not None:
      newSet.focusSegment = self.focusSegment.copy() # This attribute will contain the value of the "focus segment"
    newSet.type = self.type # Type of variation of distances for the different blocks composing the Set
    newSet.listBlockDistance = self.listBlockDistance.copy() # List of the distances of the block composing the set (in m)
    #newSet.listBlock = [] # List of the block objects that will compose the Set
    if self.variationSegment is not None:
      newSet.variationSegment = self.variationSegment.copy() # The variation object that describes the variation selected for the set. 
    newSet.sequenceType = self.sequenceType # This will indicate what type of sequence this set is: "Half-half", "buildblock", etc. 
    newSet.duration = self.duration # This will contain the duration of the set in seconds

    # Copying all the blocks
    for block in self.listBlock:
      newBlock = block.copy()
      newSet.listBlock.append(newBlock)

    return newSet
  
  # Copy method that also changes the value of the "focus set" parameter for all the focus segments in the set
  def newFocusCopy(self, newFocusSegment):

    # newFocusSegment: dictionary which describes the new values of the focus segment

    # Starting by making a copy of the Set
    newSet = self.copy()

    # Changing the value of the focus segment attribute
    newSet.focusSegment = newFocusSegment.copy()

    # Then looping on all the blocks
    for block in self.listBlock:

      # Then loopping on all the segments
      for segment in block.listSegment:

        # In the case where the segment is the focus of the block
        if segment.focus:

          # Looping on all the parameters of the block
          for parameter in settings.globals.listAllParameters:
            segment.setForcedParameter(parameterName=parameter,
                                       parameterValue=newFocusSegment[parameter])
            
    # finalising the Set - Just to make sure that the durations are right
    newSet.finalise()

    return newSet         


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

  # Dictionary method for the API outputs
  def dictionary(self):

    listBlockDictionary = []
    for block in self.listBlock:
      listBlockDictionary.append(block.dictionary())

    setDictionary = {"setType": self.type,
                     "setTime": self.duration,
                     "setDistance": self.distance,
                     "listBlock": listBlockDictionary}
    
    return setDictionary
