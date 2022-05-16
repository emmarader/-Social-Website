from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db = SQLAlchemy(app)

db.create_all()

class LocationModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Integer, nullable=False)
    longitude = db.Column(db.Integer, nullable=False)
    number_people = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Location(ID={self.id}, latitude={self.latitude}, longitude={self.longitude}, number people={self.number_people})"

resource_fields = {
    "location_id": fields.Integer,
    "latitude": fields.Integer,
    "longitude": fields.Integer,
    "number_people": fields.Integer
}

class Location(Resource):
    @marshal_with(resource_fields)
    def get(self, location_id):
        result = LocationModel.query.filter_by(id=location_id).first()
        if not result:
            abort(404, message="could not find video with that id")
        return result
    
    @marshal_with(resource_fields)
    def put(self, location_id):
        args = location_put_args.parse_args()
        result = LocationModel.query.filter_by(id=location_id).first()
        if result:
            abort(409, message="location id taken")
        location = LocationModel(id=location_id, id=args["id"], latitude=args["latitude"], longitude=args["longitude"], number_people=["number_people"])

        db.session.commit()
        return location, 201

    @marshal_with(resource_fields)
    def patch(self, location_id):
        args = location_update_args.parse_args()
        result = LocationModel.query.filter_by(id=location_id).first()
        if not result:
            abort(404, message="location does not exist, cant update")

        # This checks if name value is not None
        if args["location_id"]:
            result.id = args["location_id"]

        db.session.add(result)
        db.session.commit()
        return result

location_put_args = reqparse.RequestParser()
# required = True will show error instead of showing None
location_put_args.add_argument("latitude", type=str, help="latitude of the location is required", required=True)
location_put_args.add_argument("longitude", type=int, help="longitude of the location is required", required=True)
location_put_args.add_argument("number people", type=int, help="number of people")

location_update_args = reqparse.RequestParser()
location_put_args.add_argument("latitude", type=str, help="latitude of the location")
location_put_args.add_argument("longitude", type=int, help="longitude of the location")
location_put_args.add_argument("number people", type=int, help="number of people")


if __name__ == "__main__":
    # TODO REMOVE DEBUG=TRUE BEFORE PUSH
    app.run(debug=True)