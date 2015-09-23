from flask import Flask, jsonify, request
from flask.ext.cors import CORS
from firebase import firebase
import json, os, random
from kafka_producer.parking_producer import parking_data_producer
from kafka_producer.gps_producer import gps_data_producer

app = Flask(__name__)
cors = CORS(app, allow_headers='Content-Type')

@app.route("/get_parking_data", methods=['GET'])
def get_parking_data():
    firebase1 = firebase.FirebaseApplication('https://publicdata-parking.firebaseio.com', None)
    result = firebase1.get('/', None)

    # format the input data
    streets = result['san_francisco']['streets']

    # remove geofire
    if '_geofire' in streets:
        streets.pop('_geofire')

    for i in streets:
        streets[i]['open_spaces'] = random.randint(0,5)
        streets[i]['points'] = streets[i]['points'][:2]
    lines = json.dumps(result)
    parking_data_producer(lines)
    return lines

@app.route("/save_parking_data", methods=['GET'])
def save_parking_data():
    firebase1 = firebase.FirebaseApplication('https://publicdata-parking.firebaseio.com', None)
    result = firebase1.get('/', None)
    with open('d2.txt','w') as f:
        f.write(json.dumps(result))
    f.close()
    return json.dumps(result)

@app.route("/save_parking_data2", methods=['GET'])
def save_parking_data2():
    firebase1 = firebase.FirebaseApplication('https://publicdata-parking.firebaseio.com', None)
    result = firebase1.get('/', None)
    result.pop('streets')
    return json.dumps(result)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    app.run(debug=True)
