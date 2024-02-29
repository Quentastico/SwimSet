# IMPORTS

import numpy as np
import globals

class Variation:

    # Definition of the initialisation function
    def __init__(self, allowedVariation, varyingParameters):

        # ATTRIBUTES
        self.allowedVariation = allowedVariation # Dictonary that defines what types of variations are allowed for this case for each segment parameter
        self.varyingParameters = varyingParameters # Dictonary that defines what values the different parameters can take though this variation
        self.selParameter = None
        self.selParameterValues = []
        self.selParameterVariation = []

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

        # Looping on all the possible parameters
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
                        indexValue = globals.strokeTypes.index(value)
                        probaValue = globals.strokeProba[indexValue]
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

        return parameterValues