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

                # Special case of stroke
                if parameter == "stroke": 

                    # Then we need to determine the actual number of strokes based on user preferences (i.e. coeffs from 0 to 1): 
                    allowedStrokes = []
                    for stroke in self.varyingParameters[parameter]:
                        indexStroke = globals.strokeTypes.index("IM")
                        probaStroke = globals.strokeProba[indexStroke]
                        if probaStroke > 0:
                            allowedStrokes.append(stroke)
                    
                    # Then we need to store the possible values of the stroke (if any)
                    if len(allowedStrokes) > 0:
                        parameterValues["stroke"] = allowedStrokes
                    
                    else:
                        parameterValues["stroke"] = None

                else: 
                    parameterValues["stroke"] = None

                # Special case of Equipment
                




