from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import json

with open('secret.json') as f:
    SECRET = json.load(f)

DB_URI = "mysql+mysqlconnector://{user}:{password}@{host}:{port}/{db}?auth_plugin=mysql_native_password".format(
    user=SECRET["user"],
    password=SECRET["password"],
    host=SECRET["host"],
    port=SECRET["port"],
    db=SECRET["db"])

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Hose(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price_in_uah = db.Column(db.Integer, unique=False)
    weight_in_gramms = db.Column(db.Integer, unique=False)
    length_in_meters = db.Column(db.Integer, unique=False)
    thickness_in_milimetres = db.Column(db.Integer, unique=False)
    diameter_in_centimetres = db.Column(db.Integer, unique=False)

    def __init__(self, price_in_uah=0, weight_in_gramms=0, length_in_meters=0, thickness_in_milimetres=0,
                 diameter_in_centimetres=0):
        self.price_in_uah = price_in_uah
        self.weight_in_gramms = weight_in_gramms
        self.length_in_meters = length_in_meters
        self.thickness_in_milimetres = thickness_in_milimetres
        self.diameter_in_centimetres = diameter_in_centimetres


class HoseSchema(ma.Schema):
    class Meta:
        fields = ('id', 'price_in_uah', 'weight_in_gramms', 'length_in_meters', 'thickness_in_milimetres',
                  'diameter_in_centimetres')


hose_schema = HoseSchema()
hoses_schema = HoseSchema(many=True)


def check_if_object_exists(obj):
    if not obj:
        return abort(404)


@app.route("/hose", methods=["POST"])
def add_hose():
    price_in_uah = request.json['price_in_uah']
    weight_in_gramms = request.json['weight_in_gramms']
    length_in_meters = request.json['length_in_meters']
    thickness_in_milimetres = request.json['thickness_in_milimetres']
    diameter_in_centimetres = request.json['diameter_in_centimetres']

    new_hose = Hose(price_in_uah, weight_in_gramms, length_in_meters, thickness_in_milimetres, diameter_in_centimetres)
    db.session.add(new_hose)
    db.session.commit()
    return hose_schema.jsonify(new_hose)


@app.route("/hose", methods=["GET"])
def get_hoses():
    all_hoses = Hose.query.all()
    result = hoses_schema.dump(all_hoses)
    return jsonify({'hoses': result})


@app.route("/hose/<id>", methods=["GET"])
def get_single_hose(id):
    hose = Hose.query.get(id)

    check_if_object_exists(hose)

    return hose_schema.jsonify(hose)


@app.route("/hose/<id>", methods=["PUT"])
def smart_home_appliance_update(id):
    hose = Hose.query.get(id)

    check_if_object_exists(hose)

    hose.price_in_uah = request.json['price_in_uah']
    hose.weight_in_gramms = request.json['weight_in_gramms']
    hose.diameter_in_centimetres = request.json['diameter_in_centimetres']
    hose.length_in_meters = request.json['length_in_meters']
    hose.thickness_in_milimetres = request.json['thickness_in_milimetres']

    db.session.commit()
    return hose_schema.jsonify(hose)


@app.route("/hose/<id>", methods=["DELETE"])
def smart_home_appliance_delete(id):
    hose = Hose.query.get(id)

    check_if_object_exists(hose)

    db.session.delete(hose)
    db.session.commit()
    return f"hose with id {hose.id} deleted"


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
