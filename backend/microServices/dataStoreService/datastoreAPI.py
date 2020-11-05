import re
import json
from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

# -== Helper functions ==-

# Return the info about a machine from DB
def GetMachineInfo(Name):
    cleanName = str(re.sub("[^0-9a-zA-Z]", "", str(Name)))
    # Open file as JSON
    dbFile = open("./staticDB/machines.json")
    allMachines = json.load(dbFile)
    # Look if the name exists in file
    # TODO: Optimize from linear search to something faster, when DB gets bigger
    for machine in allMachines:
        if str(machine["name"]) == str(cleanName):
            return machine
    return False # as no machine was found

# -== Params ==-
port = 8855

# -== Endpoint functionality ==-
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

# -== Endpoints ==-
api.add_resource(MachineInfo, "/machineInfo")

# -== Start server ==-
# Validate input, if correct then start server
if int(port) >= 0 and int(port) <= 65535: 
    app.run(threaded=True, debug=False, port=int(port), host="0.0.0.0")