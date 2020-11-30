import re
import json
import requests
from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

# -== Helper functions ==-

# Limit the amount of valid input chars, to increase security
def LimitInputChars(string):
    return str(re.sub("[^0-9a-zA-Z-=',:.! ]", "", str(string)))

# Get the IP(s) of machines within a category, as list
def GetCategoryIPs(category):
    global machines
    attackers = []

    # Find all of category, and get their IP
    for machine in machines:
        if machine["category"] == str(category):
            attackers.append(machine["ip"])
    return attackers

# -== Params ==-
port = 8855
machines = []
started = False

# -== Endpoint functionality ==-

# Each call will add a machine to the machines, list
class AddMachine(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id")
        parser.add_argument("ip")
        parser.add_argument("category")
        args = parser.parse_args()

        # Store data in dict
        machineInfo = {
            "id": LimitInputChars(args["id"]),
            "ip": LimitInputChars(args["ip"]),
            "category": LimitInputChars(args["category"])
        }
        
        # Add machineInfo to list
        global machines
        machines.append(machineInfo)
        return "Machine Added"

# Called to start the campagign
class Start(Resource):
    def post(self):
        global started
        if not started:
            started = True
            parser = reqparse.RequestParser()
            parser.add_argument("waitTimeMin")
            args = parser.parse_args()

            # Get attacker IP(s) and send start request to attacker
            attackerIPs = GetCategoryIPs("attacker")
            defenderIPs = GetCategoryIPs("defender")
            #for attackerIP in attackerIPs:
                #requests.post("http://" + str(attackerIP) + "/start")
                # TODO: Add the needed params for the attacker to start

            return "Started"
        else:
            return "ERROR: Campaign already started"

# -== Endpoints ==-
api.add_resource(AddMachine, "/addMachine")
api.add_resource(Start, "/start")

# -== Start server ==-
# Validate input, if correct then start server
if int(port) >= 0 and int(port) <= 65535: 
    app.run(threaded=True, debug=False, port=int(port), host="0.0.0.0")