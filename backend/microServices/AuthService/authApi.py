import re
from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

# -== Helper functions ==-

# Limit the amount of valid input chars, to increase security
def LimitInputChars(string):
    return str(re.sub("[^0-9a-zA-Z_\-.: ]", "", str(string)))

# -== Params ==-
apiKey = ""
port = 8855

# -== Endpoint functionality ==-
class Auth(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("key")
        args = parser.parse_args()
        global apiKey
        if str(LimitInputChars(args["key"])) == str(apiKey):
            return "Valid" 
        else:
            return "Invalid"

class InitKey(Resource):
    def post(self):
        # Only initialize the first time this is called
        global apiKey
        if str(apiKey) == "":
            parser = reqparse.RequestParser()
            parser.add_argument("key")
            args = parser.parse_args()
            apiKey = str(LimitInputChars(args["key"]))
            return "Key initialized"
        else:
            return "Key already initialized!"

# -== Endpoints ==-
api.add_resource(Auth, "/auth")
api.add_resource(InitKey, "/initKey")

# -== Start server ==-
# Validate input, if correct then start server
if int(port) >= 0 and int(port) <= 65535: 
    app.run(threaded=True, debug=False, port=int(port), host="0.0.0.0")