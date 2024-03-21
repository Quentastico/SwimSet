# IMPORTS

import numpy as np


#TRAINING

# Minimum total distance for a training session (m)
# Note: this distance includes the cooldown, warmup and main set
minTotalDistance = 600

# Minimum warmup distance for any size of training set (m)
# Note: This is the absolute minimal distance to warm up - this value is therefore set higher than the minimal value minTotalDistance!
minWarmupDistance = 200

# Usual percentage of warmup distance compared to the total distance (0-1)
# Note: This will be how the warmup distance is calculated in practice: 
# for example, for a 4000m set, it is expected that the warmup distance will be 4000 * fracWarmupDistane (e.g. 800m if fracWarmupDistance = 0.2)
fracWarmupDistance = 0.2

# Maximum cooldown distance (m)
# Note: We do not want the cool down to exceed a certain distance which is set at maxCoolDownDistance
maxCooldownDistance = 300

# Usual percentage of cooldown distance compared to the total distance (0-1)
# Note: Process to set the cool down is as follows: the cooldown starts at 100m and then should increase by 100m by slice of 1500m for the total set
# The cooldown distance still has a max (see above)
fracCooldownDistance = 1/15

## SET

# Minimal Set Distance (m)
# Note: this is the minimal distance of any given set - Note that this distance must be consitent with the minTotalDistance, the minWarmupDistance
# and the starting cooldown distance (100m)
minSetDistance = 300

# Average Set distance (m)
# The average set distance provides a key element when setting the various distance sets - this info is used to skewed the distribution of set distances. 
# The higher the avSetDistance, the longer the sets. 
avSetDistance = 600

# Minimum denominator of all the sets in a given training session
# Example: if 100, then all set distances will be multiple of 100m. 
stepSetDistance = 100

# Maximal acceptable distance between the set required distance and the actual distance
maxDistanceDiff = 50

# Defining the different types of variation withtin a set
# This describes the different types of sets that exist in term of the distance variation from one block to the other. 
# equal: Means that all blocks within the set will have the same distance
# increasing: Means that the distance will increase steadily from one block to the other
# decreasing: Means that the distance will decrease steadily from one block to the other
# pyramid: Means that the distance will increase and then decrease. 
# setTypes = ["equalDistance",
#             "increasingDistance",
#             "decreasingDistance",
#             "pyramidDistance",
#             "distanceRep", 
#             ""]

# Minimal difference distance between two blocks (m)
# If this variable is set at 25m, this means that we could have a set where the blocks are for example 25m, 50m, 75m, etc. If set at 50m, then the 
# minimal distance between two sets will be set at 50m, etc. 
stepBlockDistance = 50

# Minimal number of blocks in the case of an "increase" type of set
# For example, if this is set at 3, then this means that the miminal number of blocks in an "increase" of the distance variation will be three blocks. 
minBlocksIncrease = 3

# Minimal number of blocks in the case of a "decrease" type of set
# Same as above, but for sets with an decreasing distance from one block to the other
minBlocksDecrease = 3

# Minimal number of blocks in the case of a pyramid
# For example, if set to 3, this measn that the pyramid will have 3 blocks (2 increase and 1 decrease)
minBlocksPyramid = 3

## CONSTANT DISTANCE SET

# Distribution of probabilities between random split of segments from one block to another (case 1) of non-random split (case 2)
splitTypeConstantDistance = ["randomSplit", "increaseDecreaseSplit"]
splitProbaConstantDistance = [0.5, 0.5]

# Definition of the parameters that can change from one block to the other for different types of sets

# Case 1: Constant distance with non-changing block
allowedVariationConstantDistance1 = {"stroke": ["cycle"], 
                                  "equipment": ["cycle"],
                                  "intensity": ["increase", "decrease"],
                                  "drill": ["cycle"], 
                                  "kick": None}

# Case 2.1 : Constant distance with increasing distance first segment
allowedVariationConstantDistance21 = {"stroke": None, 
                                  "equipment": None,
                                  "intensity": ["decrease"],
                                  "drill": None, 
                                  "kick": None}

# Case 2.2: Constant distance with decreasing distance first segment
allowedVariationConstantDistance22 = {"stroke": None, 
                                  "equipment": None,
                                  "intensity": ["increase"],
                                  "drill": None, 
                                  "kick": None}

## INCREASING/DECREASING DISTANCE SET

# Note that values below are set mainly for a set which block decrease in length

# Distribution of the increase vs. decrease
# Note: this is also used for the Distance Rep sets
increaseDecreaseType = ["increase", "decrease"]
increaseDecreaseProba = [0.5, 0.5]

# Distribution of probabilities between the different cases
# Case 1: Only one segment per block
# Case 2: Each block will be split in 2 halves
# Case 3: Each block will be split in a constant + increasing length
# Case 4: Each block will build toward a full block
splitTypeIncreaseDecreaseDistance = ["singleSegment", "halfHalf", "constantChanging", "buildBlock"]
splitProbaIncreaseDecreaseDistance = [0.25, 0.25, 0.25, 0.25]

# Case 1: Only one segment per block
allowedVariationIncreaseDecreaseDistance1 = {"stroke": None,
                                             "equipment": None,
                                             "intensity": ["increase"],
                                             "drill": None,
                                             "kick": None}

# Case 2: Two segment with the same distance each ("half-half")
allowedVariationIncreaseDecreaseDistance2 = {"stroke": None,
                                             "equipment": None,
                                             "intensity": ["increase"],
                                             "drill": None,
                                             "kick": None}

# Case 3: Two segments with a constant distance and a changing distance
allowedVariationIncreaseDecreaseDistance3 = {"stroke": None,
                                             "equipment": None,
                                             "intensity": ["increase"],
                                             "drill": None,
                                             "kick": None}

# Case 4: each block is the addition of Nblock segments
allowedVariationIncreaseDecreaseDistance4 = {"stroke": ["cycle"],
                                             "equipment": None,
                                             "intensity": ["increase", "decrease"],
                                             "drill": ["cycle"],
                                             "kick": None}

## DISTANCE REP SET

# For distance rep sets, this ratio indicates the maximum ratio of the total distance that can be covered by a block of a given distance
# For example, in a 600m "distance rep" set; if the ratio is 0.5, this means that the maximal distance that can be covered by a block of a given distance is 300m.
# In this example, this means that we cannot have more than 6 times 50m, or more than 3 times 100m, etc. 
ratioDistanceRep = 0.5

# Case 1: Only one segment per block - Only case considered
# Note that this is valid for a set with an increase in the distance (which is the case when building blocks) - The blocks
# can be flipped at the end of the build process
allowedVariationDistanceRep1 = {"stroke": None,
                                "equipment": None,
                                "intensity": ["decrease"],
                                "drill": None,
                                "kick": None}

## FREQUENCY INCREASE SET

# These parameters fix the min and max numbers of Blocks in the frequency increase set
# for example, if min = 2 and max = 4, then there will be either 2, 3 or 4 blocks in the frequency increase
# Note, if this value is equal to 3, and lets say that the selected segment length is 50m, then that means that the set will be made of: 
# - A first block with 3 * 3 50m, with something happening (e.g. fast) every third 50m
# - A second block with 3 * 2 50m, with something happening (e.g. fast) every second 50m
# - A third block with 3 * 1 50m, with something happening (e.g. fast) every 50m
minNumberFrequencyIncrease = 2
maxNumberFrequencyIncrease = 4

# Case 1: As many segment as required in each block
# The "allowed variation" is here defined between the base segment and the special segment
allowedVariationFrequencyIncrease1 = {"stroke": ["cycle"],
                                "equipment": None,
                                "intensity": ["increase"],
                                "drill": None,
                                "kick": ["cycle"]}

## BLOCK

# Minimum and maximum values for a block distance (m)
# Note: For any given block, this fixes the minimal distance. 
minBlockDistance = 50
maxBlockDistance = 500

# Minimum number of segments per block
# If fixed at 2, this means that unless forced otherwise, the minimal number of segments will be 2 in any block. 
# Note that for some types of sets (for example pyramid, increasing or decreasing, we do not allow the blocks to change)
minSegmentNumber = 1

# Maximum number of segments per block
# Same as above. 
maxSegmentNumber = 2


## SEGMENT

# List of the diufferent parameters that characterises a segment
listAllParameters = ["stroke", "equipment", "intensity", "drill", "kick"]

# Minimum value for a segment distance (m)
# Note: A value of 25m is recommended as this will fit any pool (25m or 50m)
minSegmentDistance = 25

# Maximum value for the distance of a segment (m)
# Note: this maximal value for a segment distance can be superseded in the case of a non "equal" set type as we force the segment distance to be 
# equal to the block distance. 
maxSegmentDistance = 300

# Step distance between two segments
# Example: if this is 25m, this means that two segments must have a minimal distance difference of 25m between themselves. 
stepSegmentDistance = 25

# Definition of the possible equipment
equipmentTypes = ["pullBuoyAndPaddles", "fins", "No equipment"]
equipmentProba = [0.1, 0.2, 0.7]

# Definition of the possible variations of kicks
kickTypes = ["kick", "No kick"]
kickProba = [0.1, 0.9]

# Definition of the possible variations of drill
drillTypes = ["drill", "No drill"]
drillProba = [0.1, 0.9]

# Definition of the different types of stroke
strokeTypes = ["freestyle", "breaststroke", "backstroke", "butterfly", "IM"]
strokeProba = [0.6, 0.1, 0.1, 0.1, 0.1]

# Definition of the types of intensity
# The intensity usually varies from 4 to 10; anything under 4 is considered as being very slow, so the minIntensity is not set at 1; 
# 10 is typically the maximal intensity and the intensity is usllay increased by an increment of 1. 
minIntensity = 4
maxIntensity = 10
stepIntensity = 1

# Definition of the path to the excel spreadsheet for the variation of parameters from one block to the other in a set
segmentConstraintsPath = "/content/SwimSet/segmentConstraints.xlsx"

# Definition of the path to the excel setting the constraints on the "base segment(s)" in a block (i.e. the non-changing segment)
baseSegmentPath = "/content/SwimSet/baseSegment.xlsx"

# Definition of the "base" times for different strokes, equipment, etc. 
# Note: All the times below are in seconds
# Note: all the times are based on Quentin's perception for now

# Base time in the "base conditions" (s)
baseTime = 105

# Definition of the "base conditions"
baseTimeParameters = {"distance": 100,
                      "intensity": 5,
                      "stroke": "freestyle",
                      "equipment": "No equipment",
                      "drill": "No drill",
                      "kick": "no kick"}

# Times for the different strokes (i.e. for the stroke being listed as in strokeTypes; all other parameters being defined in baseTimeParameters)
baseTimeStroke = [105, 150, 135, 150, 135]

# Times for the different equipmment (i.e. for the equipment being listed as in equipmentTypes; all other parameters being defined in baseTimeParameters)
baseTimeEquipment = [105, 95, 105]

# Times for the different drills (i.e. for the drill being listed as in strokeTypes; all other parameters being defined in baseTimeParameters)
baseTimeDrill = [120, 105]

# Times for the different kicks (i.e. for the stroke being listed as in kickTypes; all other parameters being defined in baseTimeParameters)
baseTimeKick = [150, 105]

# Times for the different intensities (i.e. between 4 and 10); all other parameters being defined in baseTimeParameters
baseTimeIntensity = [120, 105, 110, 120, 130, 140, 150]

# Creating a dictionary indicating the base times for each parameter variation
baseTimes = {"stroke": baseTimeStroke,
             "equipment": baseTimeEquipment,
             "drill": baseTimeDrill,
             "kick": baseTimeKick,
             "intensity": baseTimeIntensity}

# Creating a dictionary listing all the values of parameters
baseTimeTypes = {"stroke": strokeTypes,
                 "equipment": equipmentTypes,
                 "drill": drillTypes,
                 "kick": kickTypes,
                 "intensity": list(np.arange(minIntensity, maxIntensity+1, 1))}
