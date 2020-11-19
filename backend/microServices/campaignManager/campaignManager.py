import re
import uuid
import json
import base64
from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

# -== Helper functions ==-

# Limit the amount of valid input chars, to increase security
def LimitInputChars(string):
    return str(re.sub("[^0-9a-zA-Z-=]", "", str(string)))

# Send required info to attacker machine, in order to start the attack
def StartAttacker(waitTimeMin):
    global machines
    allMachines = list(str(machines))
    attackerIP = ""

    return len(allMachines)

    # Get IP of attacker
    for i in list(machines):
        return

    return attackerIP

# -== Params ==-
apiKey = LimitInputChars(uuid.uuid4)
port = 8855
machines = None

# -== Endpoint functionality ==-
class Init(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("machineInfo")
        parser.add_argument("waitTimeMin")
        args = parser.parse_args()

        # Decode the machine info from base64
        machineInfoBytes = LimitInputChars(args["machineInfo"]).encode("ascii")
        decodedMachineInfo = base64.b64decode(machineInfoBytes).decode("ascii")
        global machines
        machines = json.dumps('"' + str(decodedMachineInfo) + '"')[0]

        # Start the attacker machine
        return machines[0]
        return StartAttacker(int(args["waitTimeMin"]))

        return machines

# -== Endpoints ==-
api.add_resource(Init, "/init")

# -== Start server ==-
# Validate input, if correct then start server
if int(port) >= 0 and int(port) <= 65535: 
    app.run(threaded=True, debug=False, port=int(port), host="0.0.0.0")