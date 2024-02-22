## GLOBAL VARIABLES

import numpy as np
import globals
from utils import cutSetStaged
from utils import cutSetDistanceRep
from Block import Block
from Set import Set
import utils

class ConstantDistanceSet(Set):

    def __init__(self, distance):
        super().__init__(distance)

    
