from flask import Flask, make_response, render_template
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

# -== Helper functions ==-
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

# -== Endpoints ==-
api.add_resource(Root, "/")
api.add_resource(CSS, "/css")

# -== Start server ==-
def StartServer(Port):
    app.run(threaded=True, debug=True, port=Port, host="0.0.0.0")