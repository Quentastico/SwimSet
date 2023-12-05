import globals
import numpy as np

class Segment:

  # Initialisation function
  def __init__ (self, distance, randomDef = True):

    #Attributes
    self.distance = distance # Segment distance in m
    self.randomDef = randomDef # If True, then the segment characteristics are defined randomly.
    self.stroke = None # Segment stroke
    self.equipment = None # Equipment used fior this segment
    self.intensity = None # Intensity of the training
    self.duration = None # Duration of the segment (in seconds)

    if self.randomDef:

      self.setStroke()
      self.setEquipment()
      self.setIntensity()


  # Method setting  the stroke
  # Note: Maybe add an option for freestyle only, freestyle and form only, and drill + breath pattern + kicks optional
  # Maybe adjust the strokes to the distance (e.g. if higher than 150m, maybe no form, etc. )
  def setStroke(self):
    self.stroke = globals.strokeTypes[np.random.randint(low = 0, high = len(globals.strokeTypes))]

  # Method to set the equipment
  # Maybe add options to make sure that combinations make sense (fly + pull is not great)
  # Add an option for the user to decide if they want any equipment at all
  def setEquipment(self):
    self.equipment = globals.equipmentTypes[np.random.randint(low = 0, high = len(globals.equipmentTypes))]

  # Method to set the intensity
  # Same thng: Maybe have a think of when the intensity makes sense...
  def setIntensity(self):
    self.intensity = np.random.randint(low = globals.minIntensity, high = globals.maxIntensity + 1)

  # Method to dsplay the infos of a given segment
  def info(self):
    print("This segment is " + self.stroke + ", has a distance of " + str(self.distance) + ", " + str(self.equipment) + " for equipment, and intensity of " + str(self.intensity))

  # Method to set the duration
  # Here instead of random, there is a need to calculate the right duration as a function of everything else