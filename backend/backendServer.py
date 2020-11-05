import sys
import requests
import re
import json
import urllib
from flask import Flask, make_response, render_template, request
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from app.dockerController import SpawnContainer, GetContainerIP
from app.vagrantController import SpawnVagrantMachine, GetMachineIP

app = Flask(__name__)
api = Api(app)
CORS(app)

# -== SpawnMicroServices ==-
authService = SpawnContainer("auth_service:latest")
authServiceIP = GetContainerIP(authService)
datastoreService = SpawnContainer("datastore_service:latest")
datastoreServiceIP = GetContainerIP(datastoreService)

# -== Helper functions ==-

# Function to return file and mime-type, as a Flask response
# Note: File has to be in ./templates folder
def MakeResponse(fileLocation, mimeType):
    response = make_response(render_template(fileLocation))
    response.headers['Content-Type'] = mimeType
    return response

# Validate key, by making a request to the auth micro service
def ValidateKey(key):
    req = requests.post("http://" + authServiceIP + ":8855/auth?key=" + key)
    responseText = LimitInputChars(req.text)
    if str(responseText) == str("Valid"):
        return True
    else:
        return False 

# Limit the amount of valid input chars, to increase security
def LimitInputChars(string):
    return str(re.sub("[^0-9a-zA-Z_\-.: ]", "", str(string)))

# Check if machine exists, and return info if it does
def GetMachineInfo(Name):
    req = urllib.request.urlopen("http://" + datastoreServiceIP + ":8855/machineInfo?name=" + Name)
    if(req.getcode() == 200):
        data = req.read()
        if str(LimitInputChars(data.decode("ascii"))) == str("Invalid"):
            return False
        else:
            return json.loads(data)

# -== Endpoint functionality ==-

# Spawn a machine if API key is correct, and machine exists
class SpawnMachine(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("key")
        parser.add_argument("machineName")
        args = parser.parse_args()

        # Make sure API key is correct
        if ValidateKey(str(LimitInputChars(args["key"]))):
            # Make sure machine exists, and which type to spawn
            machineInfo = GetMachineInfo(str(LimitInputChars(args["machineName"])))
            # If no machine is found
            if machineInfo == False:
                return "Invalid Machine"
            # If it is a Vagrant machine
            elif str(machineInfo["type"]) == "vagrant":
                spawned = SpawnVagrantMachine(machineInfo["pathFromRoot"])
                if spawned == True:
                    return "Spawn," + str(machineInfo["name"]) + "," + str(GetMachineIP(str(machineInfo["pathFromRoot"])))
                else:
                    return "Failed to spawn :("
            # If it is a Docker machine
            elif str(machineInfo["type"]) == "docker":
                try:
                    spawnID = SpawnContainer(str(machineInfo["imageName"]))
                    spawnIP = GetContainerIP(spawnID)
                    return "Spawn," + str(spawnID) + "," + str(spawnIP)
                except:
                    return "Failed to spawn :("
        else:
            return "Invalid key"

# -== Endpoints ==-
api.add_resource(SpawnMachine, "/spawnMachine")

# -== Start server ==-
# Validate input, if correct then start server
port = sys.argv[1]
if int(port) >= 0 and int(port) <= 65535: 
    app.run(threaded=True, debug=False, port=int(port), host="0.0.0.0")