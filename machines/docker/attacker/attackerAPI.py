import re
import os
from flask import Flask, jsonify,request
from flask_restful import Resource, Api, reqparse
from subprocess import Popen

app = Flask(__name__)
api = Api(app)

# -== stored variables ==-
campaignResult = {"info":"script not ran yet"}
# -== Helper functions ==-

# Limit the amount of valid input chars, to increase security
def LimitInputChars(string):
    return str(re.sub("[^0-9a-zA-Z-]", "", str(string)))

# -== Params ==-
started = False
port = 8855

# -== Endpoint functionality ==-
class Start(Resource):
    def post(self):
        global started
        if not apiKey:
            own_ip  = os.popen('ip addr show eth0 | grep "\<inet\>" | awk \'{ print $2 }\' | awk -F "/" \'{ print $1 }\'').read().strip()
            parser = reqparse.RequestParser()
            parser.add_argument("ipToUse")
            parser.add_argument("waitTime")
            parser.add_argument("attackType")
            args = parser.parse_args()
            apiKey = LimitInputChars(args["key"])
            Popen("cd " + str(args["attackType"]) + "; ./exploit.sh " + str(args["ipToUse"]) + " " + own_ip+ " " + str(args["waitTime"]) + " ")
            apiKey = True
            return "Started script"
        else:
            return "ERROR, machine already started!"


#Post to the campaign manager how the attack went.
class Info(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        global campaignResult
        campaignResult =  json_data
        return "posted data."

    def get(self):
        global campaignResult
        return campaignResult


# -== Endpoints ==-
api.add_resource(Start, "/start")
api.add_resource(Info, "/info")

# -== Start server ==-
# Validate input, if correct then start server
if int(port) >= 0 and int(port) <= 65535: 
    app.run(threaded=True, debug=False, port=int(port), host="0.0.0.0")