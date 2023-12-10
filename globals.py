#TRAINING

# Minimum total distance for a set
minTotalDistance = 500

# Minimum warmup distance for any size of training set (m)
minWarmupDistance = 200

# Usual percentage of warmup distance compared to the total distance
fracWarmupDistance = 0.2

# Rules to follow for the cool down: Cooldown distrance should start at 100m and then should increase by 100m by slice of 1500m - Max should be 300m
fracCooldownDistance = 1/15
maxCooldownDistance = 300

# Minimal Set Distance
minSetDistance = 300

# Average Set distance
avSetDistance = 600



## SET

# Defining the different types of variation withtin a set
variationTypes = ["equal", "increasing", "decreasing", "pyramid"]

# What is the minimal difference between two blocks (various routines)
stepBlockDistance = 25

# Minimal number of blocks in the case of an "increase" type of set
minBlocksIncrease = 3

# Minimal number of blocks in the case of a decrease type of set
minBlocksDecrease = 3

# Minimal number of blocks in the case of a pyramid (divided by 2)
minBlocksPyramid = 2


## BLOCK

# Minimum value for a block distance (m)
minBlockDistance = 50

# Minimum and maximum numbers of segments per block
minSegmentNumber = 2
maxSegmentNumber = 3

# Options considered for the variation of intensity from one block to the other
optionIntensity = {"equal": ["intensityIncrease", "intensityConstant"], 
                   "increasing": ["intensityDecrease", "intensityConstant"], 
                   "decreasing": ["intensityIncrease", "intensityConstant"], 
                   "pyramid":["intensityConstant"]}

## SEGMENT

# Minimum value for a segment distance (m)
minSegmentDistance = 25

# Maximum value for the distance of a segment (m)
maxSegmentDistance = 300

# Step of increase between two segments (m)
stepSegmentDistance = 25

# Definition of the different types of stroke
strokeTypes = ["freestyle", "form", "drill", "breathPattern", "kick"]

# Definition of the possible equipment
equipmentTypes = ["pullBuoy", "fins", "paddles", None]

# Definition of the types of intensity
minIntensity = 1
maxIntensity = 10
stepIntensity = 1