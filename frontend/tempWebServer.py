import sys
from flask import Flask, make_response, render_template
from flask_restful import Resource, Api
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)

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
        return MakeResponse("index.html", "text/html")

class CSS(Resource):
    def get(self):
        return MakeResponse("style.css", "text/css")

class JS(Resource):
    def get(self):
        return MakeResponse("trainingPlatform.js", "text/javascript")

# -== Endpoints ==-
api.add_resource(Root, "/")
api.add_resource(CSS, "/css")
api.add_resource(JS, "/js")

# -== Start server ==-
# Validate input, if correct then start server
port = sys.argv[1]
if int(port) >= 0 and int(port) <= 65535: 
    app.run(threaded=True, debug=False, port=int(port), host="0.0.0.0")