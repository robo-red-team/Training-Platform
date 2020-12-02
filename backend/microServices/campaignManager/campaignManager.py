import re
import json
import requests
import threading
import base64
import time
from flask import Flask, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

# -== Helper functions ==-

# Limit the amount of valid input chars, to increase security
def LimitInputChars(string):
    return str(re.sub("[^0-9a-zA-Z-=',:.! ]", "", str(string)))

# Get the IP(s) of machines within a category, as list
def GetCategoryMachines(category):
    global machines
    attackers = []

    # Find all of category, and get their IP
    for machine in machines:
        if machine["category"] == str(category):
            attackers.append(machine)
    return attackers

# Base64 encode a string
def Base64EncodeString(text):
    return base64.b64encode(str(text).encode("ascii")).decode("ascii")

# Used to destroy containers after campaign
def DestroyThreads(ip, waitTime):
    global machines
    time.sleep(waitTime)
    requests.delete("http://" + str(ip) + ":8855/campaignRemove?containerIDs=" + Base64EncodeString(json.dumps(machines)))

# -== Params ==-
port = 8855
machines = []
started = False
timeFromAttackToDestroyMin = 5

# -== Endpoint functionality ==-



# Each call will add a machine to the machines, list
class AddMachine(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id")
        parser.add_argument("ip")
        parser.add_argument("category")
        parser.add_argument("name")
        args = parser.parse_args()

        # Store data in dict
        machineInfo = {
            "id": LimitInputChars(args["id"]),
            "ip": LimitInputChars(args["ip"]),
            "category": LimitInputChars(args["category"]),
            "name": LimitInputChars(args["name"])
        }
        
        # Add machineInfo to list
        global machines
        machines.append(machineInfo)
        return "Machine Added"

# Called to start the campagign
class Start(Resource):
    def post(self):
        global started
        global timeFromAttackToDestroyMin

        if not started:
            started = True
            parser = reqparse.RequestParser()
            parser.add_argument("waitTimeMin")
            
            args = parser.parse_args()

            # Get attacker IP(s) and send start request to attacker
            attackers = GetCategoryMachines("attacker")
            defenders = GetCategoryMachines("defender")
            for attacker,defender in zip(attackers,defenders):
                topost = "http://" + attacker["ip"] + ":8855/start?waitTime="+str(args["waitTimeMin"])+"&ipToUse="+defender["ip"]+"&attackType="+defender["name"]
                requests.post(topost)

            # Queue request to remove containers, once the machines are done
            mainAPI_IP = request.remote_addr
            waitBeforeDestructMin = int(args["waitTimeMin"]) + int(timeFromAttackToDestroyMin)
            waitBeforeDestructSec = waitBeforeDestructMin * 60
            thread = threading.Thread(target=DestroyThreads, args=(str(mainAPI_IP), int(waitBeforeDestructSec)))
            thread.start()
            return "Started"
        else:
            return "ERROR: Campaign already started"

# Get campaign results from attacker machine
class CampaignResults(Resource):
    def get(self):
        attackers = GetCategoryMachines("attacker")
        results=[]
        for attacker in attackers:
            req = requests.get("http://"+attacker["ip"]+":8855/"+"info")
            results.append(json.loads(req.text))
        return results 

# -== Endpoints ==-
api.add_resource(AddMachine, "/addMachine")
api.add_resource(Start, "/start")
api.add_resource(CampaignResults, "/campaignResults")

# -== Start server ==-
# Validate input, if correct then start server
if int(port) >= 0 and int(port) <= 65535: 
    app.run(threaded=True, debug=False, port=int(port), host="0.0.0.0")