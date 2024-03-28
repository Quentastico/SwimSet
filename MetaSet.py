import numpy as np
import globals

class MetaSet:

    # Initialisation function
    def __init__(self, distance, setType, numberSets):

        # Definition of attributes
        self.distance = distance # The distance of the set that will be repeated in the MetaSet (in m)
        self.setType = setType # The type of sets that will be created among the collection of sets
        self.numberSets = numberSets # The number of repeats for this set in the meta set
        self.neutralSegment = {}
        self.listFocusSegments = []

    # Method to select the neutral segment
    def selectNeutralSegment(self):

        # Here just copying the neutral segment
        self.neutralSegment = globals.metaSetNeutralSegment

    # Method to select the focus segment
    def selectFocusSegment(self):

        # Here we first import the metaSetPatterns from globals and the probabilities for each pattern
        metaSetPatterns = globals.metaSetPatterns
        metaSetPatternProba = globals.metaSetPatternProba

        # We also need to import the different probabilities reflecting user preferences
        segmentParameterTypeProba = globals.segmentParameterTypeProba

        # Then for each pattern, we want to determine if this is compatible with the user choices (e.g. fins, etc.)
        filteredPatterns = {}

        # Here pattern is the name of a pattern
        for pattern in metaSetPatterns.keys(): 

            # Here creating a list of dictionaries that will list all possible combos in a given pattern
            filteredPatterns[pattern] = []

            # Here parameterSet is a dictionary of single values for equipment, stroke, etc. 
            for parameterSet in metaSetPatterns[pattern]:

                validParameterSet = True

                for parameter in parameterSet.keys():

                    if parameter != "intensity":

                        # 1. Determining the value of this parameter in this specific pattern part
                        forcedValue = parameterSet[parameter]

                        # 2. Determining the corresponding probability of this parameter in the user preferences
                        forcedValueIndex = segmentParameterTypeProba[parameter][0].index(forcedValue)
                        forcedValueProba = segmentParameterTypeProba[parameter][1][forcedValueIndex]

                        # 3. Then testing if the value is 0, then we need to exclude the parameter set from the pattern
                        if forcedValueProba == 0:
                            validParameterSet = False
        
                # Testing is this is a valid parameter set
                if validParameterSet:

                    filteredPatterns[pattern].append(parameterSet)

        # Then we need to select patterns based on their length - They need to have at least as many dictionaries as the number of sets

        # Determining what pattern is valid and creating the proba vector
        validPatterns = []
        validPatternProba = []
        for pattern in filteredPatterns.keys():
            if len(filteredPatterns[pattern]) >= self.numberSets:
                validPatterns.append(pattern)
                validPatternProba.append(metaSetPatternProba[pattern])

        # Then making sure that there is at least one pattern that works
        if len(validPatterns) > 0:

            # redefining the validPatternProba
            sumProba = sum(validPatternProba)
            for i in np.arange(validPatternProba):
                validPatternProba[i] = validPatternProba/sumProba

            # Then picking a pattern randomly from validPatterns
            selPattern = np.random.choice(validPatterns, p=validPatternProba)

            # Then we need to pick from the filtered pattern numberSet different segments
            listFocusSegments = []

            availableParameterSet = filteredPatterns[selPattern]

            for i in np.arange(self.numberSets):

                # Picking a random parameter set
                selParameterSet = np.random.choice(availableParameterSet)

                # Adding the set to the list
                listFocusSegments.append(selParameterSet)

                # Removing the selected set
                availableParameterSet.pop(selParameterSet)

            # Finally stroing the value in the attribute
            self.listFocusSegments = listFocusSegments

        else: 

            print("No pattern available with the user choices")