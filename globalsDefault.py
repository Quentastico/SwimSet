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

# Defining the diffferent training types that we'll have the probability that we want for them to happen
# Random Training: the training will be split in a number of sets of random distances
# Set Rep Training: the set will be split between a number of repetition of the same set + some random ones
trainingTypes = ["Random Training", "Set Rep Training"]
trainingProba = [0.5, 0.5]

# In the case of a Set Rep Training, the following parameters must be defined: 
# The minimal and maximal numbers of repetition of the same set
minNumberRepeatSet = 2
maxNumberRepeatSet = 5

# The maximal distance of a repeated set (based onthe max of the distance rep set), in m
maxRepeatSetDistance = 700

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

# Defining the different types of variation withtin a set and associating an object type
setTypes = ["Constant Distance",
            "Increasing/Decreasing Distance", 
            "Pyramid Distance",
            "Distance Rep",
            "Frequency Increase",
            "Cyclic Distance"]

# Defining the probability of picking any type of any set randomly
setProba = [1/6, 1/6, 1/6, 1/6, 1/6, 1/6]

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
# Note that the following aplies to PyramidDistanceSet and CyclicDistanceSet

# Note that values below are set mainly for a set which block decrease in length

# Distribution of the increase vs. decrease
# Note: this is also used for the Distance Rep sets
increaseDecreaseType = ["increase", "decrease"]
increaseDecreaseProba = [0.5, 0.5]

# Minimal number of blocks in the case of an "increase" type of set
# For example, if this is set at 3, then this means that the miminal number of blocks in an "increase" of the distance variation will be three blocks. 
minBlocksIncrease = 3

# Minimal number of blocks in the case of a "decrease" type of set
# Same as above, but for sets with an decreasing distance from one block to the other
minBlocksDecrease = 3

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


# PYRAMID SET

# Minimal number of blocks in the case of a pyramid
# For example, if set to 3, this measn that the pyramid will have 3 blocks (2 increase and 1 decrease)
minBlocksPyramid = 3

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

# Maximal distance allowed for a distance Rep Set - To avoid very long calculations
maxDistanceRepDistance = 700

## FREQUENCY INCREASE SET

# These parameters fix the min and max numbers of Blocks in the frequency increase set
# for example, if min = 2 and max = 4, then there will be either 2, 3 or 4 blocks in the frequency increase
# Note, if this value is equal to 3, and lets say that the selected segment length is 50m, then that means that the set will be made of: 
# - A first block with 3 * 3 50m, with something happening (e.g. fast) every third 50m
# - A second block with 3 * 2 50m, with something happening (e.g. fast) every second 50m
# - A third block with 3 * 1 50m, with something happening (e.g. fast) every 50m
minNumberFrequencyIncrease = 2
maxNumberFrequencyIncrease = 4

# The "allowed variation" is here defined between the base segment and the special segment
allowedVariationFrequencyIncrease1 = {"stroke": ["cycle"],
                                "equipment": None,
                                "intensity": ["increase"],
                                "drill": None,
                                "kick": ["cycle"]}

## META SETS
# This section of the file describes the patterns that "meta sets" can have (these sets are repeats of the same set with with one thing 
# changing from one to the other)

# In these patterns we define the neutral segment
metaSetNeutralSegment = {"stroke": "freestyle",
                         "equipment": "No equipment",
                         "intensity": 5,
                         "drill": "No drill",
                         "kick": "No kick"} 

# Pattern 1: The "Everything"
# This pattern reflects "Fast free", "Fast form", "Fins", "Pull", "Kick"
metaSetPatternEverything = [{"stroke": "freestyle",
                             "equipment": "No equipment",
                             "intensity": 8,
                             "drill": "No drill",
                             "kick": "No kick"},
                             {"stroke": "backstroke",
                             "equipment": "No equipment",
                             "intensity": 8,
                             "drill": "No drill",
                             "kick": "No kick"},
                             {"stroke": "breaststroke",
                             "equipment": "No equipment",
                             "intensity": 8,
                             "drill": "No drill",
                             "kick": "No kick"},
                             {"stroke": "butterfly",
                             "equipment": "No equipment",
                             "intensity": 8,
                             "drill": "No drill",
                             "kick": "No kick"},
                             {"stroke": "IM",
                             "equipment": "No equipment",
                             "intensity": 8,
                             "drill": "No drill",
                             "kick": "No kick"},
                             {"stroke": "freestyle",
                             "equipment": "fins",
                             "intensity": 8,
                             "drill": "No drill",
                             "kick": "No kick"},
                             {"stroke": "freestyle",
                             "equipment": "pullBuoyAndPaddles",
                             "intensity": 8,
                             "drill": "No drill",
                             "kick": "No kick"},
                             {"stroke": "freestyle",
                             "equipment": "No equipment",
                             "intensity": 5,
                             "drill": "No drill",
                             "kick": "kick"}]

# Pattern 2: Multi Strokes
# This pattern alternates between different strokes: "IM", "backstroke", "breaststroke", "butterfly", "freestyle"
metaSetPatternStrokes = [{"stroke": "IM",
                          "equipment": "No equipment",
                          "intensity": 8,
                          "drill": "No drill",
                          "kick": "No kick"}, 
                          {"stroke": "backstroke",
                          "equipment": "No equipment",
                          "intensity": 8,
                          "drill": "No drill",
                          "kick": "No kick"}, 
                          {"stroke": "breaststroke",
                          "equipment": "No equipment",
                          "intensity": 8,
                          "drill": "No drill",
                          "kick": "No kick"},
                          {"stroke": "butterfly",
                          "equipment": "No equipment",
                          "intensity": 8,
                          "drill": "No drill",
                          "kick": "No kick"}, 
                          {"stroke": "freestyle",
                          "equipment": "No equipment",
                          "intensity": 8,
                          "drill": "No drill",
                          "kick": "No kick"}]

# Pattern 3: Multi Equipment
# This pattern alternates between different equipment: "No equipment", "fins", "pullBuoyAndPaddles"
metaSetPatternEquipment = [{"stroke": "freestyle",
                            "equipment": "No equipment",
                            "intensity": 8,
                            "drill": "No drill",
                            "kick": "No kick"},
                            {"stroke": "freestyle",
                            "equipment": "fins",
                            "intensity": 8,
                            "drill": "No drill",
                            "kick": "No kick"},
                            {"stroke": "freestyle",
                            "equipment": "pullBuoyAndPaddles",
                            "intensity": 8,
                            "drill": "No drill",
                            "kick": "No kick"}]

# Just listing all the patterns in a dictionary
metaSetPatterns = {"everything": metaSetPatternEverything,
                   "stroke": metaSetPatternStrokes,
                   "equipment": metaSetPatternEquipment}

metaSetPatternProba = {"everything": 1/3,
                       "stroke": 1/3, 
                       "equipment": 1/3}

## BLOCK

# Minimum and maximum values for a block distance (m)
# Note: For any given block, this fixes the minimal distance. 
minBlockDistance = 50
maxBlockDistance = 500

# Minimal difference distance between two blocks (m)
# If this variable is set at 25m, this means that we could have a set where the blocks are for example 25m, 50m, 75m, etc. If set at 50m, then the 
# minimal distance between two sets will be set at 50m, etc. 
stepBlockDistance = 50

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
equipmentProba = [0.1, 0.1, 0.8]

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

# Creating a dictionary listing all these parameters, their values and their probas
segmentParameterTypeProba = {"stroke": [strokeTypes, strokeProba],
                             "equipment": [equipmentTypes, equipmentProba],
                             "intensity": [np.arange(minIntensity, maxIntensity+1, stepIntensity), []],
                             "drill": [drillTypes, drillProba],
                             "kick": [kickTypes, kickProba]}

# Definition of the path to the excel spreadsheet for the variation of parameters from one block to the other in a set
# segmentConstraintsPath = "/content/SwimSet/segmentConstraints.xlsx"
segmentConstraintsPath = "segmentConstraints.xlsx"

# Definition of the path to the excel setting the constraints on the "base segment(s)" in a block (i.e. the non-changing segment)
# baseSegmentPath = "/content/SwimSet/baseSegment.xlsx"
baseSegmentPath = "baseSegment.xlsx"

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
                      "kick": "No kick"}

# Times for the other strokes
baseTimeBreaststroke = 150 
baseTimeBackstroke = 135
baseTimeButterfly = 150
baseTimeIM = 135

# Concatenating this into a vector aligned on the strokeType vector
baseTimeStroke = [baseTime, baseTimeBreaststroke, baseTimeBackstroke, baseTimeButterfly, baseTimeIM]

# Times for the different equipmment (i.e. for the equipment being listed as in equipmentTypes; all other parameters being defined in baseTimeParameters)
baseTimePullBuoyAndPaddles = 105
baseTimeFins = 95

# Concatenating the equipment times into the same array aligned on equipmentTypes
baseTimeEquipment = [baseTimePullBuoyAndPaddles, baseTimeFins, baseTime]

# Times for drill and asscoiated array
baseTimeWithDrill = 120
baseTimeDrill = [baseTimeWithDrill, baseTime]

# Times for the different kicks
baseTimeWithKicks = 150
baseTimeKick = [baseTimeWithKicks, baseTime]

# Times for the different intensities (i.e. between 4 and 10); all other parameters being defined in baseTimeParameters
baseTimeIntensity5Excluded = [100, 110, 120, 130, 140, 150]
baseTimeIntensity = [baseTimeIntensity5Excluded[0],
                     baseTime,
                     baseTimeIntensity5Excluded[1],
                     baseTimeIntensity5Excluded[2],
                     baseTimeIntensity5Excluded[3],
                     baseTimeIntensity5Excluded[4],
                     baseTimeIntensity5Excluded[5]]

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
