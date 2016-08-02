from flask import Flask, render_template
from flask_restful import reqparse, abort, Api, Resource
import requests
import json
from flask_cors import CORS, cross_origin

app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

parser = reqparse.RequestParser()
parser.add_argument('q')
parser.add_argument('date')
parser.add_argument('from')
parser.add_argument('to')


@app.route("/")
def hello():
    return render_template('home.html')


class Airlines(Resource):
    def get(self):
        url = "http://node.locomote.com/code-task/airlines"
        params = dict({})
        req = requests.get(url=url, params=params)
        data = json.loads(req.text)
        return {"message": data}


class Airports(Resource):
    def get(self, airport):
        url = "http://node.locomote.com/code-task/airports?"
        params = dict({"q": parser.parse_args()["q"]})
        req = requests.get(url=url, params=params)
        data = json.loads(req.text)
        return {"message": data}


class Search(Resource):
    def get(self, ida):
        url = "http://node.locomote.com/code-task/flight_search/" + ida
        params = dict({"date": parser.parse_args()["date"],
                       "from": parser.parse_args()["from"],
                       "to": parser.parse_args()["to"]})
        req = requests.get(url=url, params=params)
        data = json.loads(req.text)
        return {"message": data}

api.add_resource(Airports, '/api/<airport>')
api.add_resource(Airlines, '/api/airlines')
api.add_resource(Search, '/api/search/<ida>')

if __name__ == '__main__':
    app.run(debug=True, port=3000)
