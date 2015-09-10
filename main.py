from flask import Flask, jsonify, request
from flask.ext.cors import CORS
from firebase import firebase
import json, os

app = Flask(__name__)
cors = CORS(app, allow_headers='Content-Type')

@app.route("/get_parking_data", methods=['GET'])
def get_parking_data():
    firebase1 = firebase.FirebaseApplication('https://publicdata-parking.firebaseio.com', None)
    result = firebase1.get('/', None)
    lines = json.dumps(result)
    return lines
    # with open('result.txt','w') as f:
    #     f.write(lines)

if __name__ == '__main__':
    # port = int(os.environ.get("PORT", 5000))
    # app.run(host='0.0.0.0', port=port)
    app.run(debug=True)
