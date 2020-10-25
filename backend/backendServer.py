import sys
from flask import Flask, make_response, render_template
from flask_restful import Resource, Api
from app.dockerController import SpawnContainer, GetContainerIP

app = Flask(__name__)
api = Api(app)

# -== SpawnMicroServices ==-
authService = SpawnContainer("auth_service:latest")
authServiceIP = GetContainerIP(authService)

# -== Helper functions ==-

# Function to return file and mime-type, as a Flask response
# Note: File has to be in ./templates folder
def MakeResponse(fileLocation, mimeType):
    response = make_response(render_template(fileLocation))
    response.headers['Content-Type'] = mimeType
    return response

# -== Endpoint functionality ==-
class Root(Resource):
    def get(self):
        return "I am (g)root"

# -== Endpoints ==-
api.add_resource(Root, "/")

# -== Start server ==-
# Validate input, if correct then start server
port = sys.argv[1]
if int(port) >= 0 and int(port) <= 65535: 
    app.run(threaded=True, debug=False, port=int(port), host="0.0.0.0")