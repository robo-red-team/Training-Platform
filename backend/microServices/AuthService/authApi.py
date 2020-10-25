from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

# -== Helper functions ==-
def ReadApiKey(fileName):
    keyFile = open(fileName)
    readFile = keyFile.read()
    return readFile

# -== Params ==-
apiKey = ReadApiKey("tempApiKey.txt")
port = 8855

# -== Endpoint functionality ==-
class Auth(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("key")
        args = parser.parse_args()
        if str(args["key"]) == str(apiKey):
            return "Valid" 
        else:
            return "Invalid"

# -== Endpoints ==-
api.add_resource(Auth, "/auth")

# -== Start server ==-
# Validate input, if correct then start server
if int(port) >= 0 and int(port) <= 65535: 
    app.run(threaded=True, debug=False, port=int(port), host="0.0.0.0")