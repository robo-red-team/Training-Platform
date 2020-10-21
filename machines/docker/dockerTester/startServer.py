from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Root(Resource):
    def get(self):
        return "I'm (g)root"

api.add_resource(Root, "/")
app.run(threaded=True, debug=False, port=8855, host="0.0.0.0")