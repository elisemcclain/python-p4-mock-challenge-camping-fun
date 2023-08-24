#!/usr/bin/env python3

from models import db, Activity, Camper, Signup
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

@app.route('/')
def home():
    return ''

class Campers(Resource):
    def get(self):
        campers = [c.to_dict(rules=('-signups',)) for c in Camper.query.all()]
        
        return make_response(campers, 200)

    def post(self):
        new_camper = Camper()
        
        data = request.get_json()

        try:
            for key in data:
                setattr(new_camper, key, data[key])

            db.session.add(new_camper)
            db.session.commit()
            return make_response(new_camper.to_dict(rules=('-signups',)), 201)

        except ValueError as error:
            new_error = {"error": str(error)}
            return make_response(new_error, 400)

api.add_resource(Campers, '/campers')


class CampersById(Resource):
    def get(self, id):
        campers = Camper.query.filter(Camper.id == id).first()

        if not campers:
            return make_response({"error": "Camper not found"}, 404)

        return make_response(campers.to_dict(), 200)

    def patch(self, id):
        camper = Camper.query.filter(Camper.id == id).first()
        data = request.get_json()

        if not camper:
            return make_response({"error": "Camper not found"}, 404)

        try:
            for key in data:
                setattr(camper, key, data[key])

            db.session.add(camper)
            db.session.commit()
            return make_response(camper.to_dict(rules=('-signups',)), 201)

        except ValueError as error:
            new_error = {"error": str(error)}
            return make_response(new_error, 400)

api.add_resource(CampersById, '/campers/<int:id>')


class Activities(Resource):
    def get(self):
        activities = [a.to_dict(rules=('-signups',)) for a in Activity.query.all()]
        
        return make_response(activities, 200)
        if not activities:
            return make_response({"error": "Activity not found"}, 404)

        return make_response(activities.to_dict(), 200)

api.add_resource(Activities, '/activities')

class ActivitiesById(Resource):
    def delete(self, id):
        activity = Activity.query.filter(Activity.id == id).first()
        data = request.get_json()

        if not activity:
            return make_response({"error": "Activity not found"}, 404)

        if activity:
            db.session.delete(activity)
            db.session.commit()
            return make_response({}, 204)

api.add_resource(ActivitiesById, '/activities/<int:id>')

class Signups(Resource):
    def post(self):
        new_signup = Signup()
        
        data = request.get_json()

        try:
            for key in data:
                setattr(new_signup, key, data[key])

            db.session.add(new_signup)
            db.session.commit()
            return make_response(new_signup.to_dict(rules=('-signups',)), 201)

        except ValueError as error:
            new_error = {"error": str(error)}
            return make_response(new_error, 400)

api.add_resource(Signups, '/signups')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
