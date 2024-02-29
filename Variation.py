# IMPORTS

import numpy as np
import globals

class Variation:

    # Definition of the initialisation function
    def __init__(self, allowedVariation, varyingParameters, nBlocks):

        # ATTRIBUTES
        self.allowedVariation = allowedVariation # Dictonary that defines what types of variations are allowed for this case for each segment parameter
        self.varyingParameters = varyingParameters # Dictonary that defines what values the different parameters can take though this variation
        self.nBlocks = nBlocks # Number of blocks that will compose the set
        self.selParameter = None # Parameter that will be selected for a variation from one change to the other
        self.selParameterValues = [] # Possible values of this parameter
        self.selParameterVariation = [] # Final sequence of values for the selected parameter

        # DATA CHECK

        # We need to make sure that all the parameters are defined in the two dictionaries passed as inputs
        for parameter in globals.listAllParameters:
            if parameter not in self.allowedVariation.keys():
                print("Be careful when calling the Variation object - Not all parameters have a defintiion in allowedVariation")
            if parameter not in self.varyingParameters.keys():
                print("Be careful when calling the Variation object - Not all parameters have a defintiion in allowedVariation")        

    # Definition of the function which will identify what parameters are relevant, what their values can be and how they can vary. 
    # This method then defines the parameter of interest
    def selectParameter(self):

        # Creating an empty dictionary that will inform that values are actually possible for each parameter throuhout the set
        parameterValues = {}

        # Looping on all the possible parameters and populating the dictionary listing what values each parameter can take from one set to the other
        for parameter in globals.listAllParameters:
            if (self.allowedVariation[parameter] is not None) & (self.varyingParameters[parameter] is not None):

                # Special case of stroke or equipment
                if (parameter == "stroke") | (parameter == "equipment"): 

                    # Identifying the vectors of interest
                    if parameter == "stroke":
                        parameterTypes = globals.strokeTypes
                        parameterProba = globals.strokeProba
                    
                    if parameter == "equipment":
                        parameterTypes = globals.equipmentTypes
                        parameterProba = globals.equipmentProba

                    # Then we need to determine the actual number of strokes based on user preferences (i.e. coeffs from 0 to 1): 
                    allowedValues = []
                    for value in self.varyingParameters[parameter]:
                        indexValue = parameterTypes.index(value)
                        probaValue = parameterProba[indexValue]
                        if probaValue > 0:
                            allowedValues.append(value)
                    
                    # Then we need to store the possible values of the stroke (if any)
                    if len(allowedValues) > 0:
                        parameterValues[parameter] = allowedValues
                    
                    else:
                        parameterValues[parameter] = None

                # Special case of intensity, drill or kick
                if (parameter == "intensity") | (parameter == "kick") | (parameter == "drill"):

                    # Here we simply use the value "Any" normally used in self.varyingParameters
                    parameterValues[parameter] = self.varyingParameters[parameter]                    

            else: 
                parameterValues[parameter] = None

        # Then selecting the parameter that will vary from one block to the other
        possibleParameters = []
        for parameter in parameterValues.keys():
            if parameterValues[parameter] is not None:
                possibleParameters.append(parameter)

        if len(possibleParameters) > 0:
            self.selParameter = possibleParameters[np.random.randint(0,len(possibleParameters))]
            self.selParameterValues = parameterValues[self.selParameter]
        else:
            self.selParameter = None
            self.selParameterValues = []

    # Definition of the method that creates a variation
    # Note: this method can only be executed when the parameter and associated values have been selected. 
    def createVariation(self):

        # Case 1: This is a stroke variation
        if self.selParameter == "stroke":
            self.createStrokeVariation()

        # Case 2: This is an equipment variation
        if self.selParameter == "equipment":
            self.createEquipmentVariation()

        # Case 3: This is an intensity variation
        if self.selParameter == "intensity":
            self.createIntensityVariation()
        
        # Case 4: This is a drill variation
        if self.selParameter == "drill":
            self.createDrillVariation()
    
    # Defintiion of of a stroke variation (this function should only be called by createVariation)
    def createStrokeVariation(self):

        # definition of useful arrays
        strokes = self.selParameterValues
        strokesProba = []

        # Building the associated probabilties array for the possible strokes
        for stroke in strokes:
            indexStroke = globals.strokeTypes.index(stroke)
            strokesProba.append(globals.strokeProba[indexStroke])

        # The overall idea is to maximise the number of strokes that we include in the Variation
        # For example, if nBlocks is a multiple of 5, then we rotate through the 5 strokes (if they are available), etc. 
        # If we end up on a prime number higher than 5 (e.g. 7) then we simply alternate the strokes. 

        # 1. Determining the biggest number of strokes we can include
        n = len(strokes)

        while (self.nBlocks / n) != np.floor(self.nBlocks / n):
            n -= 1

        if n == 1: 
            n = 2

        # 2. Picking n random strokes from the strokes array
        selStrokes = []
        while n > 0:

            print("n: " + str(n))

            # 1. Make sure that the proba vector sums to 1
            sumProba = np.sum(strokesProba)
            for i in np.arange(len(strokesProba)):
                strokesProba[i] = strokesProba[i]/sumProba

            print("strokes")
            print(strokes)
            print("strokesProba")
            print(strokesProba)
            
            # 2. First of all adding a random stroke
            randomStroke = np.random.choice(strokes, p=strokesProba)
            selStrokes.append(randomStroke)

            print("random stroke")
            print(randomStroke)

            # Then removing from strokes and strokeProba the selected one
            indexStroke = strokes.index(randomStroke)
            strokesProba.pop(indexStroke)
            strokes.remove(randomStroke)

            # Changing the value of n
            n -= 1

        # 3. Now that the strokes are selected, we simply create the variation
        for i in np.arange(self.nBlocks):
            self.selParameterVariation.append(selStrokes[i % len(selStrokes)])
            














    
