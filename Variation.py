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
                    parameterValues[parameter] = "Any"

            else: 
                parameterValues[parameter] = None

        # Then selecting the parameter that will vary from one block to the other - Here we need to make sure that apart from "Any" value, each paramater has at least 2 values alllowed
        possibleParameters = []
        for parameter in parameterValues.keys():
            if parameterValues[parameter] is not None:
                if parameterValues[parameter] == "Any" | len(parameterValues[parameter])>1:
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
            self.createStrokeEquipmentVariation()

        # Case 2: This is an equipment variation
        if self.selParameter == "equipment":
            self.createStrokeEquipmentVariation()

        # Case 3: This is an intensity variation
        if self.selParameter == "intensity":
            self.createIntensityVariation()
        
        # Case 4: This is a drill variation
        if self.selParameter == "drill":
            self.createDrillVariation()
    
    # Definition of a stroke or equipment variation (this function should only be called by createVariation)
    def createStrokeEquipmentVariation(self):

        # definition of useful arrays
        selParameterValues = self.selParameterValues
        valuesProba = []

        # Building the associated probabilties array for the possible strokes/equipment

        # Identifying the vectors of interest
        if self.selParameter == "stroke":
            parameterTypes = globals.strokeTypes
            parameterProba = globals.strokeProba
        
        if self.selParameter == "equipment":
            parameterTypes = globals.equipmentTypes
            parameterProba = globals.equipmentProba
            
        for value in selParameterValues:
            indexValue = parameterTypes.index(value)
            valuesProba.append(parameterProba[indexValue])

        # The overall idea is to maximise the number of strokes/equipment that we include in the Variation
        # For example, if nBlocks is a multiple of 5, then we rotate through the strokes/equipment (if they are available), etc. 
        # If we end up on a prime number higher than 5 (e.g. 7) then we simply alternate the strokes/equipment. 

        # 1. Determining the biggest number of strokes/equipment we can include
        n = len(selParameterValues)

        while (self.nBlocks / n) != np.floor(self.nBlocks / n):
            n -= 1

        if n == 1: 
            n = 2

        # 2. Picking n random strokes/equipment from the strokes/equipment array
        selValues = []
        while n > 0:

            # 1. Make sure that the proba vector sums to 1
            sumProba = np.sum(valuesProba)
            for i in np.arange(len(valuesProba)):
                valuesProba[i] = valuesProba[i]/sumProba
            
            # 2. First of all adding a random strokes/equipment
            randomValue = np.random.choice(selParameterValues, p=valuesProba)
            selValues.append(randomValue)

            # Then removing from strokes/equipment and valuesProba the selected one
            indexValue = selParameterValues.index(randomValue)
            valuesProba.pop(indexValue)
            selParameterValues.remove(randomValue)

            # Changing the value of n
            n -= 1

        # 3. Now that the strokes are selected, we simply create the variation
        for i in np.arange(self.nBlocks):
            self.selParameterVariation.append(selValues[i % len(selValues)])

    # Definition of an intensity variation
    def createIntensityVariation(self):       
            
        # Import useful parameters
        maxIntensity = globals.maxIntensity
        minIntensity = globals.minIntensity

        # determining if the intensity will increase or decrease
        optionIntensity = np.random.choice(self.allowedVariation[self.selParameter])
       
        # Defining the number of intensities possible
        numIntensities = (maxIntensity-minIntensity+1)
       
        # Case 1: The number of possible intensities is higher than the number of blocks: easy, we just find intensities which increase/decrease from one block to another
        if numIntensities >= self.nBlocks:
            lowestIntensity = np.random.randint(low=minIntensity, high=maxIntensity-self.nBlocks+2)
          
            # Case 1.1: Increasing intensity
            if optionIntensity == "increase":
                for i in np.arange(self.nBlocks):
                    self.selParameterVariation.append(lowestIntensity+i)

            # Case 1.2: Decreasing intensity
            if optionIntensity == "decrease":
                for i in np.arange(self.nBlocks):
                    self.selParameterVariation.append(lowestIntensity+self.nBlocks-1-i)
    
        # Case 2: The number of possible intensities is lower than the number of blocks: we have to split them in different schemes
        else: 

            # First we need to find the maximal possible length of a series
            maxWidthIntensity = numIntensities
            while np.floor(self.nBlocks/maxWidthIntensity) != self.nBlocks / maxWidthIntensity: 
                maxWidthIntensity -= 1

            # Case 2.1: There is a number higher than 1 of options
            if maxWidthIntensity > 1: 

                lowestIntensity = np.random.randint(low=minIntensity, high=maxIntensity-maxWidthIntensity+2)

                # Case 2.1.1: Increasing intensity
                if optionIntensity == "increase":
                    for series in np.arange(np.floor(self.nBlocks/maxWidthIntensity)):
                        for i in np.arange(maxWidthIntensity):
                            self.selParameterVariation.append(lowestIntensity+i)

                # Case 2.1.2: Decreasing intensity
                if optionIntensity == "decrease":
                    for series in np.arange(np.floor(self.nBlocks/maxWidthIntensity)):
                        for i in np.arange(maxWidthIntensity):
                            self.selParameterVariation.append(lowestIntensity+maxWidthIntensity-1-i)

            # Case 2.2: The number of blocks cannot be divided by any other number than 1 (prime number)
            else: 
                # Here we make the choice that we will extend the range of intensities as much as possible even if this means that the block will not be exact
                maxWidthIntensity = numIntensities

                # Case 2.2.1: Increasing intensity
                if optionIntensity == "increase": 
                    nSeries = np.floor(self.nBlocks/maxWidthIntensity)

                    # First adding all the complete series
                    for series in np.arange(nSeries):
                        for i in np.arange(maxWidthIntensity):
                            self.selParameterVariation.append(minIntensity+i)

                    # Then adding the rest
                    for i in np.arange(self.nBlocks-nSeries*maxWidthIntensity):
                        self.selParameterVariation.append(int(minIntensity+i))

                # Case 2.2.2: Decreasing intensity
                if optionIntensity == "intensityDecrease": 
                    nSeries = np.floor(self.nBlocks/maxWidthIntensity)

                    # First adding all the complete series
                    for series in np.arange(nSeries):
                        for i in np.arange(maxWidthIntensity):
                            self.selParameterVariation.append(maxIntensity-i)

                    # Then adding the rest
                    for i in np.arange(self.nBlocks-nSeries*maxWidthIntensity):
                        self.selParameterVariation.append(int(maxIntensity-i))
    
    # Method that creates a drill variation
    def createDrillVariation(self):

        # Here the strategy is simply to offer to go through drill 1, drill 2, etc. 
        for i in np.arange(self.nBlocks):
            self.selParameterVariation.append("drill " + str(i+1))