import re
import os
from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

# -== Helper functions ==-

# Limit the amount of valid input chars, to increase security
def LimitInputChars(string):
    return str(re.sub("[^0-9a-zA-Z-]", "", str(string)))

# -== Params ==-
apiKey = ""
port = 8855

# -== Endpoint functionality ==-
class Start(Resource):
    def post(self):
        global apiKey
        if apiKey == "":
            parser = reqparse.RequestParser()
            parser.add_argument("key")
            parser.add_argument("ipToUse")
            parser.add_argument("waitTime")
            args = parser.parse_args()
            apiKey = LimitInputChars(args["key"])
            os.system("echo './exploit.sh" + str(args["ipToUse"]) + " " + str(args["waitTime"]) + "'")
            return "Started script"
        else:
            return "ERROR, machine already started!"

# -== Endpoints ==-
api.add_resource(Start, "/start")

# -== Start server ==-
# Validate input, if correct then start server
if int(port) >= 0 and int(port) <= 65535: 
    app.run(threaded=True, debug=False, port=int(port), host="0.0.0.0")