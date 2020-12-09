import sys
import requests
import re
import json
import urllib
import time
import base64
import glob
import os
import threading
from flask import Flask, make_response, render_template, request, send_file, abort
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from app.dockerController import SpawnContainer, GetContainerIP, SpawnContainerWithPass, StopContainer
from app.vagrantController import SpawnVagrantMachine, GetMachineIP

app = Flask(__name__)
api = Api(app)
CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

# -== Params ==-
waitTimeForContainerSpawn = 3

# -== Helper functions ==-

def WaitAndDeleteFile(fileLocation):
    time.sleep(5)
    print(fileLocation, file=sys.stderr)
    os.remove(fileLocation)
    
# Function to return file and mime-type, as a Flask response
# Note: File has to be in ./templates folder
def MakeResponse(fileLocation, mimeType):
    response = make_response(render_template(fileLocation))
    response.headers["Content-Type"] = mimeType
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
    return str(re.sub("[^0-9a-zA-Z_\-.: \/?=&]", "", str(string)))

# Get JSON data from API, given the URL with params
def GetJSONDataFromAPI(UrlWithParams):
    req = urllib.request.urlopen(str(LimitInputChars(UrlWithParams)))
    if(req.getcode() == 200):
        data = req.read()
        if str(LimitInputChars(data.decode("ascii"))) == str("Invalid"):
            return False
        else:
            return json.loads(data)

# Initialize key in Auth Service
def InitAuthKey(MachineIP):
    # Give the container time to spawn, then send request to init key
    time.sleep(waitTimeForContainerSpawn)
    cleanKey = str(LimitInputChars(sys.argv[2]))
    requests.post("http://" + str(MachineIP) + ":8855/initKey?key=" + str(cleanKey))

# Spawn a machine, based upon the machine name
def SpawnMachine(MachineName):
    # Make sure machine exists, and which type to spawn
    machineInfo = GetJSONDataFromAPI("http://" + datastoreServiceIP + ":8855/machineInfo?name=" + str(LimitInputChars(MachineName)))
    # If no machine is found
    if machineInfo == False:
        return False
    # If it is a Vagrant machine
    elif str(machineInfo["type"]) == "vagrant":
        spawned = SpawnVagrantMachine(machineInfo["pathFromRoot"])
        if spawned == True:
            return {"id": str(machineInfo["name"]), "ip": str(GetMachineIP(str(machineInfo["pathFromRoot"]))), "attacker": machineInfo["attacker"], "shortDescription": machineInfo["shortDescription"]}
        else:
            return False
    # If it is a Docker machine
    elif str(machineInfo["type"]) == "docker":
        try:

            if str(machineInfo["category"]) == "defender":
                retdict = SpawnContainerWithPass(str(machineInfo["imageName"]))
                spawnID = retdict["id"]
                passwd  = retdict["password"]  
            else:
                spawnID = SpawnContainer(str(machineInfo["imageName"]))
                passwd = "No pass"
            spawnIP = GetContainerIP(spawnID)


            return {"id": str(spawnID), "ip": str(spawnIP), "category": machineInfo["category"], "shortDescription": machineInfo["shortDescription"], "password":passwd, "name":MachineName}
        except:
            return False

# Base64 encode a string
def Base64EncodeString(text):
    return base64.b64encode(str(text).encode("ascii")).decode("ascii")

# Base64 decode a string
def Base64DecodeString(text):
    return base64.b64decode(text.encode("ascii")).decode("ascii")

# -== Endpoint functionality ==-

# Spawn a campaign if API key is correct
class SpawnCampaign(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("key")
        parser.add_argument("name")
        parser.add_argument("waitTimeMin")
        args = parser.parse_args()

        # Make sure API key is correct
        if ValidateKey(str(LimitInputChars(args["key"]))):
            # Fetch data from datastore
            campaignInfo = GetJSONDataFromAPI("http://" + str(datastoreServiceIP) + ":8855/campaignInfo?name=" + str(LimitInputChars(args["name"])))
            
            # Spawn a campaign manager, and wait for it to be done
            manager = SpawnContainer("campaign-manager_service:latest")
            managerIP = GetContainerIP(manager)
            time.sleep(waitTimeForContainerSpawn)
            # Add info about the campaign manager to it's list of containers
            requests.post("http://" + str(managerIP) + ":8855/addMachine?id=" + LimitInputChars(manager) + "&ip=" + LimitInputChars(managerIP) + "&category=" + "infrastructure" + "&name=" + "campaignManager")
            
            # Spawn machines, store data in list, and send info to campaign manager
            spawnInfo = []
            for machine in campaignInfo["machines"]:
                machineInfo = SpawnMachine(machine)
                spawnInfo.append(machineInfo)
                topost = "http://" + str(managerIP) + ":8855/addMachine?id=" + LimitInputChars(machineInfo["id"]) + "&ip=" + LimitInputChars(machineInfo["ip"]) + "&category=" + LimitInputChars(machineInfo["category"]) + "&name=" +machineInfo["name"]
                requests.post(topost)

            # Ensure service have time to add all data
            time.sleep(int(waitTimeForContainerSpawn / 2))

            # Start the campaign
            requests.post("http://" + str(managerIP) + ":8855/start?waitTimeMin=" + LimitInputChars(args["waitTimeMin"]))
            
            # Return info of all spawned machines, to be displayed on the front-end 
            campaignReturn = {
                "id": Base64EncodeString(managerIP),
                "machines": spawnInfo
            }
            return campaignReturn
        else:
            abort(401)


# Send names of all campaigns
class CampaignNames(Resource):
    def get(self):
        return GetJSONDataFromAPI("http://" + datastoreServiceIP + ":8855/campaigns")

# Send public info about campaigns
class CampaignInfo(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        args = parser.parse_args()
        # Get all info, and make sure the name was correct
        allInfo = GetJSONDataFromAPI("http://" + datastoreServiceIP + ":8855/campaignInfo?name=" + str(LimitInputChars(args["name"])))
        if allInfo == False:
            return {"name": "ERROR", "description": "Error getting campaign data!"}
        else:
            return {"name": allInfo["name"], "description": allInfo["description"]}

# Get campaign results
class CampaignResults(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id")
        args = parser.parse_args()
        toreturn = requests.get("http://"+Base64DecodeString(args["id"])+":8855/"+"campaignResults")        
        return json.loads(toreturn.text)
        
# Removing all files from the machine, called after a successfull campaign
class CampaignRemoval(Resource):
    def delete(self):
        # Get data and decode it
        parser = reqparse.RequestParser()
        parser.add_argument("containerIDs")
        args = parser.parse_args()
        data = json.loads(Base64DecodeString(args["containerIDs"]))

        # Loop through all machines and stop them
        for machine in data:
            if not machine["id"] == None and not machine["id"] == "":
                StopContainer(LimitInputChars(machine["id"]))

        return "Stopped campaign machines"

# Get a VPN bundle, and delete it form this machine
class GetVPNBundle(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("key")
        args = parser.parse_args()
        
        # Make sure the key is valid
        if ValidateKey(str(LimitInputChars(args["key"]))):
            # Get all file locations
            pathToFolder = os.getcwd()
            folder = str(pathToFolder) + "/backend/vpnBundles/"
            fileLocations = glob.glob(folder + "*")
            
            # Send and delete file, if any is found
            if len(fileLocations) > 0:
                try:
                    thread = threading.Thread(target=WaitAndDeleteFile, args=(fileLocations[0],))
                    thread.start()
                    #print(fileLocations[0],file=sys.stderr)
                    return send_file(fileLocations[0], as_attachment=True, attachment_filename='RoboRedTeam.zip')
                except:
                    abort(404)
            else:
                abort(404)
        else:
            abort(401)


# -== Endpoints ==-
api.add_resource(SpawnCampaign, "/campaignSpawn")
api.add_resource(CampaignNames, "/campaignNames")
api.add_resource(CampaignInfo, "/campaignInfo")
api.add_resource(CampaignRemoval, "/campaignRemove")
api.add_resource(GetVPNBundle, "/vpnBundle")
api.add_resource(CampaignResults, "/campaignResults")



# -== SpawnMicroServices ==-
authService = SpawnContainer("auth_service:latest")
authServiceIP = GetContainerIP(authService) 
InitAuthKey(authServiceIP)
datastoreService = SpawnContainer("datastore_service:latest")
datastoreServiceIP = GetContainerIP(datastoreService)

# -== Start server ==-
# Validate input, if correct then start server
port = sys.argv[1]
if int(port) >= 0 and int(port) <= 65535: 
    app.run(threaded=True, debug=False, port=int(port), host="0.0.0.0")
