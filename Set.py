## GLOBAL VARIABLES

import numpy as np
import globals
from Block import Block
import utils

class Set:

  # Initialisation function
  def __init__(self, distance):

    # 1. ATTRIBUTES

    self.distance = distance # Distance of the set (m)
    self.type = None # Type of variation of distances for the different blocks composing the Set
    self.listBlockDistance = [] # List of the distances of the block composing the set (in m)
    self.listBlock = [] # List of the block objects that will compose the Set

  # Info method        
  def info(self):

    print("  SET - Distance: " + str(self.distance) + ", Variation of distance: " + str(self.type) + ", List of Block distances: " + str(self.listBlockDistance))
    for block in self.listBlock:
      block.info()
