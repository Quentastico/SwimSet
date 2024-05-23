import functions_framework
import json
import urllib
from Training import Training

@functions_framework.http
def generateTraining(req):

    # Extracting the data from the json
    request_json = req.get_json(silent=True)
    request_args = req.args

    # Extraction of the distance
    if request_json and 'distance' in request_json:
        distance = float(request_json['distance'])
    elif request_args and 'distance' in request_args:
        distance = float(request_args['distance'])

    # Creation of a training function
    training = Training(distance=distance, standardInit=True, verbose=0)

    return {"message": "You should see the distance you previously entered",
            "distance": distance, 
            "warmupDistance": training.warmupDistance}