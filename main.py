from flask import Flask, jsonify, request
from flask.ext.cors import CORS
from firebase import firebase
import json, os, random, datetime, time
from kafka_producer.parking_producer import parking_data_producer
from kafka_producer.gps_producer import gps_data_producer
from elasticsearch import Elasticsearch

app = Flask(__name__)
cors = CORS(app, allow_headers='Content-Type')

def conver_to_unix_time(ctime):
    time_list = ctime.split()
    # convert to unix ctime 'Tue Sep 15 15:16:58 2015'

    # convert to ctime - this is for hourly analysis and hence ignoring
    time_list = time_list[ :-2]

    temp = time_list[-1]
    time_list[-1] = time_list[-2]
    time_list[-2] = temp

    new_time = " ".join(time_list)
    b = datetime.datetime.strptime(new_time, "%a %b %d %H:%M:%S %Y")
    formatted_time = ""
    formatted_time += str(b.year)+str(b.month).zfill(2)+str(b.day).zfill(2)+'-'+str(b.hour).zfill(2)+str(b.minute).zfill(2)+str(b.second).zfill(2)
    return formatted_time


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

    # create timestamp YYYYMMDD-HHmmss
    result['san_francisco']['_updated'] = conver_to_unix_time(result['san_francisco']['_updated'])

    lines = json.dumps(result)
    parking_data_producer(lines)
    return lines

@app.route("/get_nearest_spot/<lat>/<lon>/", methods=['GET'])
def get_nearest_spot(lat, lon):
    d = {}
    d['lat'] = lat
    d['lon'] = lon
    es = Elasticsearch("http://ec2-52-3-61-194.compute-1.amazonaws.com:9200")
    INDEX_NAME = 'parktest'
    # q = '{"query":{"filtered":{"query":{"match_all":{}},"filter":{"geo_distance":{"distance":"1km","location":{"lat":37.787590,"lon":-122.400227}}}}}}'
    q = '{"query":{"filtered":{"query":{"match_all":{}},"filter":{"geo_distance":{"distance":"1km","location":{"lat":'+lat+',"lon":'+lon+'}}}}}}'
    print "query is ", q
    result = es.search(index = INDEX_NAME, size=10, body=q)
    # result = d
    lines = json.dumps(result['hits']['hits'])
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
