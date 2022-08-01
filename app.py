from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
# import os

app = Flask(__name__)
CORS(app)

# basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://bwtnzqzxuzwcsq:c4ac96db90773d9142aacc965b0495de4b43c30c2ddd5b20decd39d436fd7ec8@ec2-18-214-35-70.compute-1.amazonaws.com:5432/d75jbirfmp1s54'
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Traffic(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    type = db.Column(db.String, nullable=False)
    count = db.Column(db.Integer, nullable=False)

    def __init__(self, type, count):
        self.type = type
        self.count = count


class TrafficSchema(ma.Schema):
    class Meta:
        fields = ('id', 'type', 'count')


traffic_schema = TrafficSchema()
traffics_schema = TrafficSchema(many=True)


@app.route('/add_type', methods=['POST'])
def add_traffic_type():
    if request.content_type != 'application/json':
        return jsonify('data must be json')

    post_data = request.get_json()
    type = post_data.get('type')
    count = post_data.get('count')

    new_record = Traffic(type, count)
    db.session.add(new_record)
    db.session.commit()

    return jsonify(traffic_schema.dump(new_record))


@app.route('/delete/<id>', methods=["DELETE"])
def delete_traffic(id):
    traffic = db.session.query(Traffic).filter(Traffic.id == id).first()
    db.session.delete(traffic)
    db.session.commit()
    return jsonify('successfully deleted')


@app.route('/update_traffic/<type>', methods=["PUT"])
def update_traffic(type):
    if request.content_type != 'application/json':
        return jsonify('data must be json')
    data = request.get_json()
    count = data.get('count')

    data_to_update = db.session.query(
        Traffic).filter(Traffic.type == type).first()

    if count != None:
        data_to_update.count = count

    db.session.commit()
    return jsonify(traffic_schema.dump(data_to_update))


@app.route('/get_traffics', methods=["GET"])
def get_traffics():
    records = db.session.query(Traffic).all()
    return jsonify(traffics_schema.dump(records))


@app.route('/get_traffic/<type>', methods=["GET"])
def get_traffic(type):
    record = db.session.query(Traffic).filter(Traffic.type == type).first()
    return jsonify(traffic_schema.dump(record))


if __name__ == '__main__':
    app.run(debug=True)
