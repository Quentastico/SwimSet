import globalsDefault
import numpy as np
from utils import extractFromJSON

class Globals:

    # Initialisation function
    def __init__(self):

        # Building the globals based on the default values (see GlobalsDefault for full definitions of the arguments)
        self.minTotalDistance = globalsDefault.minTotalDistance
        self.minWarmupDistance = globalsDefault.minWarmupDistance
        self.fracWarmupDistance = globalsDefault.fracWarmupDistance
        self.maxCooldownDistance = globalsDefault.maxCooldownDistance
        self.fracCooldownDistance = globalsDefault.fracCooldownDistance
        self.trainingTypes = globalsDefault.trainingTypes
        self.trainingProba = globalsDefault.trainingProba
        self.minNumberRepeatSet = globalsDefault.minNumberRepeatSet
        self.maxNumberRepeatSet = globalsDefault.maxNumberRepeatSet
        self.maxRepeatSetDistance = globalsDefault.maxRepeatSetDistance
        self.minSetDistance = globalsDefault.minSetDistance
        self.avSetDistance = globalsDefault.avSetDistance
        self.stepSetDistance = globalsDefault.stepSetDistance
        self.maxDistanceDiff = globalsDefault.maxDistanceDiff
        self.setProba = globalsDefault.setProba
        self.splitTypeConstantDistance = globalsDefault.splitTypeConstantDistance
        self.splitProbaConstantDistance = globalsDefault.splitProbaConstantDistance
        self.allowedVariationConstantDistance1 = globalsDefault.allowedVariationConstantDistance1
        self.allowedVariationConstantDistance21 = globalsDefault.allowedVariationConstantDistance21
        self.allowedVariationConstantDistance22 = globalsDefault.allowedVariationConstantDistance22
        self.increaseDecreaseType = globalsDefault.increaseDecreaseType
        self.increaseDecreaseProba = globalsDefault.increaseDecreaseProba
        self.minBlocksIncrease = globalsDefault.minBlocksIncrease
        self.minBlocksDecrease = globalsDefault.minBlocksDecrease
        self.splitTypeIncreaseDecreaseDistance = globalsDefault.splitTypeIncreaseDecreaseDistance
        self.splitProbaIncreaseDecreaseDistance = globalsDefault.splitProbaIncreaseDecreaseDistance
        self.allowedVariationIncreaseDecreaseDistance1 = globalsDefault.allowedVariationIncreaseDecreaseDistance1
        self.allowedVariationIncreaseDecreaseDistance2 = globalsDefault.allowedVariationIncreaseDecreaseDistance2
        self.allowedVariationIncreaseDecreaseDistance3 = globalsDefault.allowedVariationIncreaseDecreaseDistance3
        self.allowedVariationIncreaseDecreaseDistance4 = globalsDefault.allowedVariationIncreaseDecreaseDistance4
        self.minBlocksPyramid = globalsDefault.minBlocksPyramid
        self.ratioDistanceRep = globalsDefault.ratioDistanceRep
        self.allowedVariationDistanceRep1 = globalsDefault.allowedVariationDistanceRep1
        self.maxDistanceRepDistance = globalsDefault.maxDistanceRepDistance
        self.minNumberFrequencyIncrease = globalsDefault.minNumberFrequencyIncrease
        self.maxNumberFrequencyIncrease = globalsDefault.maxNumberFrequencyIncrease
        self.allowedVariationFrequencyIncrease1 = globalsDefault.allowedVariationFrequencyIncrease1
        self.metaSetNeutralSegment = globalsDefault.metaSetNeutralSegment
        self.metaSetPatternEverything = globalsDefault.metaSetPatternEverything
        self.metaSetPatternStrokes = globalsDefault.metaSetPatternStrokes
        self.metaSetPatternEquipment = globalsDefault.metaSetPatternEquipment
        self.metaSetPatterns = globalsDefault.metaSetPatterns
        self.metaSetPatternProba = globalsDefault.metaSetPatternProba
        self.minBlockDistance = globalsDefault.minBlockDistance
        self.maxBlockDistance = globalsDefault.maxBlockDistance
        self.stepBlockDistance = globalsDefault.stepBlockDistance
        self.minSegmentNumber = globalsDefault.minSegmentNumber
        self.maxSegmentNumber = globalsDefault.maxSegmentNumber
        self.listAllParameters = globalsDefault.listAllParameters
        self.minSegmentDistance = globalsDefault.minSegmentDistance
        self.maxSegmentDistance = globalsDefault.maxSegmentDistance
        self.stepSegmentDistance = globalsDefault.stepSegmentDistance
        self.equipmentTypes = globalsDefault.equipmentTypes
        self.equipmentProba = globalsDefault.equipmentProba
        self.kickTypes = globalsDefault.kickTypes
        self.kickProba = globalsDefault.kickProba
        self.drillTypes = globalsDefault.drillTypes
        self.drillProba = globalsDefault.drillProba
        self.strokeTypes = globalsDefault.strokeTypes
        self.strokeProba = globalsDefault.strokeProba
        self.minIntensity = globalsDefault.minIntensity
        self.maxIntensity = globalsDefault.maxIntensity
        self.stepIntensity = globalsDefault.stepIntensity
        self.segmentParameterTypeProba = globalsDefault.segmentParameterTypeProba
        self.segmentConstraintsPath = globalsDefault.segmentConstraintsPath
        self.baseSegmentPath = globalsDefault.baseSegmentPath
        self.baseTime = globalsDefault.baseTime
        self.baseTimeParameters = globalsDefault.baseTimeParameters
        self.baseTimeBreaststroke = globalsDefault.baseTimeBreaststroke
        self.baseTimeBackstroke = globalsDefault.baseTimeBackstroke
        self.baseTimeButterfly = globalsDefault.baseTimeButterfly
        self.baseTimeIM = globalsDefault.baseTimeIM
        self.baseTimeStroke = globalsDefault.baseTimeStroke
        self.baseTimePullBuoyAndPaddles = globalsDefault.baseTimePullBuoyAndPaddles
        self.baseTimeFins = globalsDefault.baseTimeFins
        self.baseTimeEquipment = globalsDefault.baseTimeEquipment
        self.baseTimeWithDrill = globalsDefault.baseTimeWithDrill
        self.baseTimeDrill = globalsDefault.baseTimeDrill
        self.baseTimeWithKicks = globalsDefault.baseTimeWithKicks
        self.baseTimeKick = globalsDefault.baseTimeKick
        self.baseTimeIntensity5Excluded = globalsDefault.baseTimeIntensity5Excluded
        self.baseTimeIntensity = globalsDefault.baseTimeIntensity
        self.baseTimes = globalsDefault.baseTimes
        self.baseTimeTypes = globalsDefault.baseTimeTypes

    # Function that changes the values of Globals based on the user choice (in the case of an API call)
    def buildFromReq(self, requestJSON, requestArgs):

        # Changing the value of the user-defined variables if they have been defined
        self.trainingProba = extractFromJSON("trainingProba", self.trainingProba, requestJSON, requestArgs)
        self.minNumberRepeatSet = extractFromJSON("minNumberRepeatSet", self.minNumberRepeatSet, requestJSON, requestArgs)
        self.maxNumberRepeatSet = extractFromJSON("maxNumberRepeatSet", self.maxNumberRepeatSet, requestJSON, requestArgs)
        self.minSetDistance = extractFromJSON("minSetDistance", self.minSetDistance, requestJSON, requestArgs)
        self.avSetDistance = extractFromJSON("avSetDistance", self.avSetDistance, requestJSON, requestArgs)
        self.stepSetDistance = extractFromJSON("stepSetDistance", self.stepSetDistance, requestJSON, requestArgs)
        self.maxDistanceDiff = extractFromJSON("maxDistanceDiff", self.maxDistanceDiff, requestJSON, requestArgs)
        self.setProba = extractFromJSON("setProba", self.setProba, requestJSON, requestArgs)
        self.splitProbaConstantDistance = extractFromJSON("splitProbaConstantDistance", self.splitProbaConstantDistance, requestJSON, requestArgs)
        self.increaseDecreaseProba = extractFromJSON("increaseDecreaseProba", self.increaseDecreaseProba, requestJSON, requestArgs)
        self.minBlocksIncrease = extractFromJSON("minBlocksIncrease", self.minBlocksIncrease, requestJSON, requestArgs)
        self.minBlocksDecrease = extractFromJSON("minBlocksDecrease", self.minBlocksDecrease, requestJSON, requestArgs)
        self.splitProbaIncreaseDecreaseDistance = extractFromJSON("splitProbaIncreaseDecreaseDistance", self.splitProbaIncreaseDecreaseDistance, requestJSON, requestArgs)
        self.minBlocksPyramid = extractFromJSON("minBlocksPyramid", self.minBlocksPyramid, requestJSON, requestArgs)
        self.ratioDistanceRep = extractFromJSON("ratioDistanceRep", self.ratioDistanceRep, requestJSON, requestArgs)
        self.minNumberFrequencyIncrease = extractFromJSON("minNumberFrequencyIncrease", self.minNumberFrequencyIncrease, requestJSON, requestArgs)
        self.maxNumberFrequencyIncrease = extractFromJSON("maxNumberFrequencyIncrease", self.maxNumberFrequencyIncrease, requestJSON, requestArgs)
        self.minBlockDistance = extractFromJSON("minBlockDistance", self.minBlockDistance, requestJSON, requestArgs)
        self.maxBlockDistance = extractFromJSON("maxBlockDistance", self.maxBlockDistance, requestJSON, requestArgs)
        self.stepBlockDistance = extractFromJSON("stepBlockDistance", self.stepBlockDistance, requestJSON, requestArgs)
        self.minSegmentNumber = extractFromJSON("minSegmentNumber", self.minSegmentNumber, requestJSON, requestArgs)
        self.maxSegmentNumber = extractFromJSON("maxSegmentNumber", self.maxSegmentNumber, requestJSON, requestArgs)
        self.minSegmentDistance = extractFromJSON("minSegmentDistance", self.minSegmentDistance, requestJSON, requestArgs)
        self.maxSegmentDistance = extractFromJSON("maxSegmentDistance", self.maxSegmentDistance, requestJSON, requestArgs)
        self.stepSegmentDistance = extractFromJSON("stepSegmentDistance", self.stepSegmentDistance, requestJSON, requestArgs)
        self.equipmentProba = extractFromJSON("equipmentProba", self.equipmentProba, requestJSON, requestArgs)
        self.kickProba = extractFromJSON("kickProba", self.kickProba, requestJSON, requestArgs)
        self.drillProba = extractFromJSON("drillProba", self.drillProba, requestJSON, requestArgs)
        self.strokeProba = extractFromJSON("strokeProba", self.strokeProba, requestJSON, requestArgs)
        self.baseTime = extractFromJSON("baseTime", self.baseTime, requestJSON, requestArgs)
        self.baseTimeBreaststroke = extractFromJSON("baseTimeBreaststroke", self.baseTimeBreaststroke, requestJSON, requestArgs)
        self.baseTimeBackstroke = extractFromJSON("baseTimeBackstroke", self.baseTimeBackstroke, requestJSON, requestArgs)
        self.baseTimeButterfly = extractFromJSON("baseTimeButterfly", self.baseTimeButterfly, requestJSON, requestArgs)
        self.baseTimeIM = extractFromJSON("baseTimeIM", self.baseTimeIM, requestJSON, requestArgs)
        self.baseTimePullBuoyAndPaddles = extractFromJSON("baseTimePullBuoyAndPaddles", self.baseTimePullBuoyAndPaddles, requestJSON, requestArgs)
        self.baseTimeFins = extractFromJSON("baseTimeFins", self.baseTimeFins, requestJSON, requestArgs)
        self.baseTimeWithDrill = extractFromJSON("baseTimeWithDrill", self.baseTimeWithDrill, requestJSON, requestArgs)
        self.baseTimeWithKicks = extractFromJSON("baseTimeWithKicks", self.baseTimeWithKicks, requestJSON, requestArgs)
        self.baseTimeIntensity5Excluded = extractFromJSON("baseTimeIntensity5Excluded", self.baseTimeIntensity5Excluded, requestJSON, requestArgs)

        # Redefining the calculated global variables

        self.segmentParameterTypeProba = {"stroke": [self.strokeTypes, self.strokeProba],
                                          "equipment": [self.equipmentTypes, self.equipmentProba],
                                          "intensity": [np.arange(self.minIntensity, self.maxIntensity+1, self.stepIntensity), []],
                                          "drill": [self.drillTypes, self.drillProba],
                                          "kick": [self.kickTypes, self.kickProba]}
        
        self.baseTimeStroke = [self.baseTime, self.baseTimeBreaststroke, self.baseTimeBackstroke, self.baseTimeButterfly, self.baseTimeIM]

        self.baseTimeEquipment = [self.baseTimePullBuoyAndPaddles, self.baseTimeFins, self.baseTime]

        self.baseTimeDrill = [self.baseTimeWithDrill, self.baseTime]

        self.baseTimeKick = [self.baseTimeWithKicks, self.baseTime]

        self.baseTimeIntensity = [self.baseTimeIntensity5Excluded[0],
                                  self.baseTime,
                                  self.baseTimeIntensity5Excluded[1],
                                  self.baseTimeIntensity5Excluded[2],
                                  self.baseTimeIntensity5Excluded[3],
                                  self.baseTimeIntensity5Excluded[4],
                                  self.baseTimeIntensity5Excluded[5]]
        
        self.baseTimes = {"stroke": self.baseTimeStroke,
                          "equipment": self.baseTimeEquipment,
                          "drill": self.baseTimeDrill,
                          "kick": self.baseTimeKick,
                          "intensity": self.baseTimeIntensity}
        



      

