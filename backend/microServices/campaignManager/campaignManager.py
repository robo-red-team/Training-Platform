import re
import uuid
import json
from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

# -== Helper functions ==-

# Limit the amount of valid input chars, to increase security
def LimitInputChars(string):
    return str(re.sub("[^0-9a-zA-Z-]", "", str(string)))

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
        return "hello " + str(args["machineInfo"])

# -== Endpoints ==-
api.add_resource(Init, "/init")

# -== Start server ==-
# Validate input, if correct then start server
if int(port) >= 0 and int(port) <= 65535: 
    app.run(threaded=True, debug=False, port=int(port), host="0.0.0.0")