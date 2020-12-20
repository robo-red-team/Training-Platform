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

# Endpoint used to authenticate, by matching if the key is correct
class Auth(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("key")
        args = parser.parse_args()
        global apiKey

        # If the key matches what is stored, then return "Valid", otherwise return "Invalid"
        if str(LimitInputChars(args["key"])) == str(apiKey):
            return "Valid" 
        else:
            return "Invalid"

# Endpoint used to initialize key, which will only function once
class InitKey(Resource):
    def post(self):
        # Only initialize the first time this is called
        global apiKey
        if str(apiKey) == "":
            parser = reqparse.RequestParser()
            parser.add_argument("key")
            args = parser.parse_args()

            # Set the key, and return success message
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