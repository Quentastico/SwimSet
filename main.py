import functions_framework
import json
import urllib
from Training import Training
from utils import extractFromJSON
from Globals import Globals

@functions_framework.http
def generateTraining(req):

    # Extracting the data from the json
    requestJSON = req.get_json(silent=True)
    requestArgs = req.args

    # Extraction of the distance
    distance = extractFromJSON(parameterName="distance",
                               parameterDefault=None,
                               requestJSON=requestJSON,
                               requestArgs=requestArgs)
    
    # Creation of the parameter object "Globals"
    global globals
    globals = Globals()
    globals.buildFromReq(requestJSON=requestJSON,
                         requestArgs=requestArgs)

    # Creation of a training function
    training = Training(distance=distance,
                        standardInit=True,
                        verbose=0)

    # Generation of the training output
    output = training.dictionary()

    ## Generating a json compatible object
    jsonOutput = json.dumps(output, default=str)

    return jsonOutput