import globals
import numpy as np

class Segment:

  # Initialisation function
  def __init__ (self, distance, equipment = None):

    # 1. ATTRIBUTES

    self.distance = distance # Segment distance in m
    self.stroke = None # Segment stroke
    self.equipment = equipment # Equipment used for this segment
    self.intensity = None # Intensity of the training
    self.duration = None # Duration of the segment (in seconds)
    self.drill = None # Whether this segment is a drill segment (Boolean)
    self.kick = None # Whether this segment is kick (Boolean)

  # Method to set the equipment
  def setEquipment(self):

    if self.equipment == None:
      self.equipment = np.random.choice(globals.equipmentTypes, p=globals.equipmentProba)

  # Method to set the Kick
  def setKick(self):

    if self.equipment != "pullBuoyAndPaddles":
      self.kick = np.random.choice(globals.kickTypes, p=globals.kickProba)

  # Method to set the drill
  def setDrill(self):

    if self.equipment != "pullBuoyAndPaddles":
      self.drill = np.random.choice(globals.drillTypes, p=globals.drillProba)

  # Method setting  the stroke
  def setStroke(self):

    if self.equipment == "pullBuoyAndPaddles":
      self.stroke = "freestyle"
    
    else:
      self.stroke = np.random.choice(globals.strokeTypes, p=globals.strokeProba)

  # Method to set the intensity
  def setIntensity(self):
    self.intensity = np.random.randint(low = globals.minIntensity, high = globals.maxIntensity + 1)

  # Method to set all attributes
  def setAll(self):

    self.setEquipment()
    self.setKick()
    self.setDrill()
    self.setStroke()
    self.setIntensity()
  
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