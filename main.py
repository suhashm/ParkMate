from flask import Flask, jsonify, request
from flask.ext.cors import CORS
from firebase import firebase
import json, os
import parking_producer
import gps_producer

app = Flask(__name__)
cors = CORS(app, allow_headers='Content-Type')

@app.route("/get_parking_data", methods=['GET'])
def get_parking_data():
    firebase1 = firebase.FirebaseApplication('https://publicdata-parking.firebaseio.com', None)
    result = firebase1.get('/', None)
    lines = json.dumps(result)
    parking_producer.parking_data_producer(lines)
    gps_producer.gps_data_producer()
    return lines

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    app.run(debug=True)
