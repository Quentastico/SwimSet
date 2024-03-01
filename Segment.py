import globals
import numpy as np
import pandas as pd

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

  # Method to set the equipment
  def setRandomEquipment(self):

    if self.equipment == None:
      self.equipment = np.random.choice(globals.equipmentTypes, p=globals.equipmentProba)

  # Method to set the Kick
  def setRandomKick(self):

    if self.equipment != "pullBuoyAndPaddles":
      self.kick = np.random.choice(globals.kickTypes, p=globals.kickProba)

  # Method to set the drill
  def setRandomDrill(self):

    if self.equipment != "pullBuoyAndPaddles":
      self.drill = np.random.choice(globals.drillTypes, p=globals.drillProba)

  # Method setting  the stroke
  def setRandomStroke(self):

    if self.equipment == "pullBuoyAndPaddles":
      self.stroke = "freestyle"
    
    else:
      self.stroke = np.random.choice(globals.strokeTypes, p=globals.strokeProba)

  # Method to set the intensity
  def setRandomIntensity(self):
    self.intensity = np.random.randint(low = globals.minIntensity, high = globals.maxIntensity + 1)

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
    segmentConstraints = pd.read_excel(globals.segmentConstraintsPath)

    # 1. Extracting the rows of interest

    # 1.1. Adding the first two rows of the table
    relConstraints = segmentConstraints.iloc[0:2]

    # 1.2. Extracting the relevant table
    for parameter in globals.listAllParameters:
      if parameter != "intensity":
        relConstraints = pd.concat([relConstraints, segmentConstraints[(segmentConstraints['Parameter']==parameter) & (segmentConstraints['Value'] == self.getParameter(parameter))]])
      else: 
        relConstraints = pd.concat([relConstraints, segmentConstraints[(segmentConstraints['Parameter']==parameter)]])

    # 2. Then for each parameter, we need to identify what values are acceptable 

    # 2.1. First of all, we determine what parameters we will keep
    relConstraints = relConstraints.transpose().reset_index()
    nameColumns = relConstraints.columns
    relConstraints["VALID"] = relConstraints[nameColumns[-4:]].apply(lambda x: False if ((x[nameColumns[-1]]=="N") or (x[nameColumns[-2]]=="N") or (x[nameColumns[-3]]=="N") or (x[nameColumns[-4]]=="N")) else True, axis = 1)
    relParameters = pd.DataFrame(relConstraints.groupby(by=0).VALID.sum()) # Note: "0" will be the name of the column
    relParameters["KEEP"] = relParameters["VALID"].apply(lambda x: True if x>0 else False)
    selParameters = relParameters[relParameters["KEEP"]].index

    # 2.2. Then we determine what value each parameter can take
    parameterValues = {}
    for parameter in globals.listAllParameters:
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

    return newSegment

  # Method to dsplay the infos of a given segment
  def info(self):
    print("    SEGMENT: Stroke: " + str(self.stroke) + ", Distance: " + str(self.distance) + ", Equipment: " + str(self.equipment) + ", Intensity: " + str(self.intensity) + ", Drill: " + str(self.drill) + ", Kick: " + str(self.kick))