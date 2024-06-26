import numpy as np
import pandas as pd
from utils import convertDuration
import settings 
import globalsDefault

class Segment:

  # Initialisation function
  def __init__ (self, distance, equipment = None):

    # 1. ATTRIBUTES

    self.distance = distance # Segment distance in m
    self.stroke = None # Segment stroke
    self.equipment = equipment # Equipment used for this segment
    self.intensity = None # Intensity of the training
    self.duration = None # Duration of the segment (in seconds)
    self.drill = None # Whether this segment is a drill segment
    self.kick = None # Whether this segment is kick
    self.focus = False # This attribute indicates if this segment is the focus of the block (Boolean)

  # Method to set the equipment
  def setRandomEquipment(self):

    if self.equipment == None:
      self.equipment = np.random.choice(settings.globals.equipmentTypes, p=settings.globals.equipmentProba)

  # Method to set the Kick
  def setRandomKick(self):

    if self.equipment != "pullBuoyAndPaddles":
      self.kick = np.random.choice(settings.globals.kickTypes, p=settings.globals.kickProba)
    else:
      self.kick = "No kick"

  # Method to set the drill
  def setRandomDrill(self):

    if self.equipment != "pullBuoyAndPaddles":
      self.drill = np.random.choice(settings.globals.drillTypes, p=settings.globals.drillProba)
    else:
      self.drill = "No drill"

  # Method setting  the stroke
  def setRandomStroke(self):

    if self.equipment == "pullBuoyAndPaddles":
      self.stroke = "freestyle"
    
    else:
      self.stroke = np.random.choice(settings.globals.strokeTypes, p=settings.globals.strokeProba)

  # Method to set the intensity
  def setRandomIntensity(self):
    
    self.intensity = np.random.randint(low = settings.globals.minIntensity, high = settings.globals.maxIntensity + 1)

  # Method to set all attributes randomly
  def setRandomAll(self):

    self.setRandomEquipment()
    self.setRandomKick()
    self.setRandomDrill()
    self.setRandomStroke()
    self.setRandomIntensity()

  # Method to set a single value of a parameter
  def setForcedParameter(self, parameterName, parameterValue):

    if parameterName == "stroke":
      self.stroke = parameterValue
    
    if parameterName == "equipment":
      self.equipment = parameterValue

    if parameterName == "kick":
      self.kick = parameterValue

    if parameterName == "drill":
      self.drill = parameterValue

    if parameterName == "intensity":
      self.intensity = parameterValue
  
  # Method to get the value of any given parameter of the segment
  def getParameter(self, parameterName):
    # parameterName: the name of the parameter of interest

    output = None

    if parameterName == "distance":
      output = self.distance
    
    if parameterName == "stroke":
      output = self.stroke

    if parameterName == "equipment":
      output = self.equipment

    if parameterName == "intensity":
      output = self.intensity

    if parameterName == "duration":
      output = self.duration

    if parameterName == "drill":
      output = self.drill
    
    if parameterName == "kick":
      output = self.kick

    return output
  
  # Method that determines what parameters can change from one block to another
  def getVaryingParameters(self):

    # Making the segmentConstraints excel into a proper Dataframe
    segmentConstraints = pd.read_excel(settings.globals.segmentConstraintsPath)

    # 1. Extracting the rows of interest

    # 1.1. Adding the first two rows of the table
    relConstraints = segmentConstraints.iloc[0:2]

    # 1.2. Extracting the relevant table
    for parameter in settings.globals.listAllParameters:
      if parameter != "intensity":
        relConstraints = pd.concat([relConstraints, segmentConstraints[(segmentConstraints['Parameter']==parameter) & (segmentConstraints['Value'] == self.getParameter(parameter))]])
      else: 
        relConstraints = pd.concat([relConstraints, segmentConstraints[(segmentConstraints['Parameter']==parameter)]])

    # 2. Then for each parameter, we need to identify what values are acceptable 

    # 2.1. First of all, we determine what parameters we will keep
    relConstraints = relConstraints.transpose().reset_index()
    nameColumns = relConstraints.columns
    relConstraints["VALID"] = relConstraints[nameColumns[-5:]].apply(lambda x: False if ((x[nameColumns[-1]]=="N") or (x[nameColumns[-2]]=="N") or (x[nameColumns[-3]]=="N") or (x[nameColumns[-4]]=="N") or (x[nameColumns[-5]]=="N")) else True, axis = 1)
    relParameters = pd.DataFrame(relConstraints.groupby(by=0).VALID.sum()) # Note: "0" will be the name of the column
    relParameters["KEEP"] = relParameters["VALID"].apply(lambda x: True if x>0 else False)
    selParameters = relParameters[relParameters["KEEP"]].index

    # 2.2. Then we determine what value each parameter can take
    parameterValues = {}
    for parameter in settings.globals.listAllParameters:
      if parameter in selParameters:
        parameterValues[parameter] = list(relConstraints[(relConstraints[0]==parameter) & (relConstraints["VALID"])][1].values)
      else:
        parameterValues[parameter] = None

    ## 3. Finally, just for consistency with other parts of the code, we replace the "None" into actual None
    for parameter in parameterValues.keys():
      if parameterValues[parameter] is not None:
        # Case where there is only one value that is equal to "None"
        if len(parameterValues[parameter]) == 1:
          if parameterValues[parameter][0] == "None":
            parameterValues[parameter] = None
        # Case where there are multiple values
        else: 
          p = 0
          for value in parameterValues[parameter]: 
            if value == "None":
              parameterValues[parameter][p] = None
            p += 1

    return parameterValues

  # Method that determines for a given segment which varies the constraints on the other segments in the same block
  def getBaseSegmentParameters(self, selParameter):

    # 1. Importing the excel table listing the possible values for the baseSegment
    baseSegment = pd.read_excel(settings.globals.baseSegmentPath, skiprows=1)

    # 2. Transforming the table to keep the row of interest by only selecting the row which corresponds to the changing segment parameter
    if selParameter is not None: 
      selBaseSegment = baseSegment[baseSegment["changingParameter"]==selParameter].copy().reset_index()
    else:
      selBaseSegment = baseSegment[baseSegment["changingParameter"]=="None"].copy().reset_index()

    # 3. Looping on all the parameters and populating the dicionary adding constraing on the base segment
    constraintBaseSegment = {}

    for parameter in settings.globals.listAllParameters:

      constraintValue = selBaseSegment.iloc[0][parameter]

      # Test if there is a constraint (i.e. if the value in the table is different from "Any"
      if constraintValue != "Any":

        # Subcase 1 - The value is "Same"
        if constraintValue == "Same":
          constraintBaseSegment[parameter] = self.getParameter(parameterName=parameter)
        
        # SubCase 2 - The value is something else
        else:
          constraintBaseSegment[parameter] = constraintValue

    return constraintBaseSegment
  
  # Method to determine the time duration of the segment (in min + sec)
  def setDuration(self):

    # Creating the dictionnary of multiplicative factors
    multFactors = {}

    for parameter in settings.globals.listAllParameters:

      # Determining the value of this parameter for the given segment
      parameterValue = self.getParameter(parameterName=parameter)
      if parameter == "drill":        
        if "drill " in parameterValue: # Then this is "drill 1", or "drill 2", or "drill 3", etc. We need to change this to "drill":
          parameterValue = "drill"

      # Extracting the relevant values of the parameters
      relBaseTimeTypes = globalsDefault.baseTimeTypes[parameter]

      # Extracting the relevant values of the times for this parameter
      relBaseTimes = globalsDefault.baseTimes[parameter]

      # Finding the position of the parameter value in relBaseTimeTypes
      indexParameterValue = relBaseTimeTypes.index(parameterValue)

      # Extracting the relevant time for the given value
      relTime = relBaseTimes[indexParameterValue]

      # Calculating the multiplicative factor
      multFactor = relTime / globalsDefault.baseTime

      # Storing the value of the factor in the dictionary
      multFactors[parameter] = multFactor

    # Calculating the final multiplicative factor

    # First setting the "basis" multiplicative factor on the 100m free time entered by the user. 
    totalMultFactor = 1

    # Then multiplying the factor based on the other strokes. 
    for parameter in multFactors.keys():
      totalMultFactor *= multFactors[parameter]

    # Calculating the duration
    duration = settings.globals.baseTime * totalMultFactor * self.distance / settings.globals.baseTimeParameters["distance"]

    # rounding up the duration at +/-5 seconds
    durationMinutes, durationSeconds = convertDuration(duration)

    # Storing the final value of the duration
    self.duration = durationMinutes*60 + durationSeconds

  # Method to fix the parameters to remove any combo that should never happen (especially kick/drill with any non-moderate intensity)
  def fixParameters(self):

    # Kick
    if self.kick == "kick":
      self.intensity = 5

    # Drill
    if "drill " in self.drill:
      self.intensity = 5
    
  # Method that can be called at the end of the generation of a segment / block / set to fix little issues in the segment(s) and calculate time
  def finalise(self):

    self.fixParameters()
    self.setDuration()

  # Copy method
  def copy(self):

    # Initialisation of the new object
    newSegment = Segment(distance=self.distance)

    # Copying the properties
    newSegment.stroke = self.stroke
    newSegment.equipment = self.equipment
    newSegment.intensity = self.intensity
    newSegment.duration = self.duration
    newSegment.drill = self.drill
    newSegment.kick = self.kick
    newSegment.focus = self.focus

    return newSegment

  # Method to dsplay the infos of a given segment
  def info(self):

    # distance
    printDistance = str(self.distance) + "m "

    # stroke
    printStroke = self.stroke + " "

    # equipment
    if self.equipment == "No equipment":
      printEquipment = ""
    else: 
      printEquipment = self.equipment + " "

    # drill
    if self.drill == "No drill":
      printDrill = ""
    else:
      printDrill = self.drill + " "
    
    # kick
    if self.kick == "No kick":
      printKick = ""
    else:
      printKick = self.kick + " "

    # Duration
    if self.duration is not None: 
      durationMinutes, durationSeconds = convertDuration(self.duration)
      printDuration = str(durationMinutes) + "min" + str(durationSeconds) + "s"
    else: 
      printDuration = ""

    # Focus
    if self.focus:
      printFocus = " *"
    else:
      printFocus = ""

    # intensity
    printIntensity = "Intensity: " + str(self.intensity) + " "

    print("    SEGMENT: " + printDistance + printKick + printStroke + printEquipment + printDrill + printIntensity + printDuration + printFocus)

  # Function that generates a dictionary (API output)
  def dictionary(self):

    segmentDictionary = {"segmentTime": int(self.duration), 
                         "segmentDistance": int(self.distance), 
                         "segmentStroke": self.stroke,
                         "segmentEquipment": self.equipment,
                         "segmentIntensity": int(self.intensity),
                         "segmentKick": bool(self.kick == "kick"),
                         "segmentDrill": bool(self.drill != "No drill"),
                         "segmentFocus": bool(self.focus)}
    
    return segmentDictionary