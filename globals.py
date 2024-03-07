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

# Defining the different types of variation withtin a set
# This describes the different types of sets that exist in term of the distance variation from one block to the other. 
# equal: Means that all blocks within the set will have the same distance
# increasing: Means that the distance will increase steadily from one block to the other
# decreasing: Means that the distance will decrease steadily from one block to the other
# pyramid: Means that the distance will increase and then decrease. 
setTypes = ["equalDistance",
            "increasingDistance",
            "decreasingDistance",
            "pyramidDistance"]
#              "distanceRep"]

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

# Options considered for the variation of intensity from one block to the other
# This sets how the intensity can vary for different types of sets. For example if "equal" has a "intensityIncrease", this means that in a set
# where each block has the same distance, the intensity from one block to the other can increase, etc. 
# optionIntensity = {"equal": ["intensityIncrease"], 
#                   "increasing": ["intensityDecrease", "intensityConstant"], 
#                   "decreasing": ["intensityIncrease", "intensityConstant"], 
#                   "pyramid":["intensityConstant"], 
#                   "distanceRep":["intensityConstant"]}

# Options considered when all blocks in a set all have equal distance
# The process for equal blocks within a set is that we create a first block structure with one or multiple segment(s). 
# Then we change one segment in this block from one block to the other. This option lists the things that can change from a changing segment to the other. 
# optionVariationBlock = ["intensity", "stroke"]


## BLOCK

# Minimum value for a block distance (m)
# Note: For any given block, this fixes the minimal distance. 
minBlockDistance = 50

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



