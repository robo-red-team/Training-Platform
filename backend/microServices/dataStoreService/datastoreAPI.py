import re
import json
from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

# -== Helper functions ==-

# Function used to return a Json object in a file
def GetJsonObjFromFile(FileName, Name):
    cleanName = str(re.sub("[^0-9a-zA-Z]", "", str(Name)))
    # Open file as JSON
    dbFile = open(FileName)
    allObjects = json.load(dbFile)
    # Look if the name exists in file
    # TODO: Optimize from linear search to something faster, when DB gets bigger
    for obj in allObjects:
        if str(obj["name"]) == str(cleanName):
            return obj
    return False # as no object was found

# Return the info about a machine from DB
def GetMachineInfo(Name):
    return GetJsonObjFromFile("./staticDB/machines.json", Name)
    
# Return info about a campaign from DB
def GetCampaignInfo(Name):
    return GetJsonObjFromFile("./staticDB/campaigns.json", Name)

# Read campaigns, and return a list of names
def GetCampaignNames():
    # Open file as JSON
    dbFile = open("./staticDB/campaigns.json")
    allCampaigns = json.load(dbFile)
    # Make list
    campaignList = []
    for campaign in allCampaigns:
        campaignList.append(campaign["name"])
    return campaignList

# -== Params ==-
port = 8855

# -== Endpoint functionality ==-

# Get all information about a machine
class MachineInfo(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        args = parser.parse_args()

        machine = GetMachineInfo(args["name"])
        if machine == False:
            return "Invalid"
        else:
            return machine

# Get all information about a campaign
class CampaignInfo(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        args = parser.parse_args()

        campaign = GetCampaignInfo(args["name"])
        if campaign == False:
            return "Invalid"
        else:
            return campaign

# Get a list of all campaign names
class Campaigns(Resource):
    def get(self):
        return GetCampaignNames()

# -== Endpoints ==-
api.add_resource(MachineInfo, "/machineInfo")
api.add_resource(CampaignInfo, "/campaignInfo")
api.add_resource(Campaigns, "/campaigns")

# -== Start server ==-
# Validate input, if correct then start server
if int(port) >= 0 and int(port) <= 65535: 
    app.run(threaded=True, debug=False, port=int(port), host="0.0.0.0")