from flask import Flask, jsonify, request
from flask.ext.cors import CORS
from firebase import firebase
import json, os, random, datetime, time, calendar
from kafka_producer.parking_producer import parking_data_producer
from elasticsearch import Elasticsearch
from cassandra.cluster import Cluster
cluster = Cluster(['52.20.47.196'])
# cluster = Cluster(['52.3.61.194'])
session = cluster.connect('parking')

app = Flask(__name__)
cors = CORS(app, allow_headers='Content-Type')

def convert_to_unix_time(ctime):
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
    result['san_francisco']['_updated'] = convert_to_unix_time(result['san_francisco']['_updated'])

    lines = json.dumps(result)
    parking_data_producer(lines)
    return lines

@app.route("/get_nearest_spot/<spots>/<lat>/<lon>/", methods=['GET'])
def get_nearest_spot(spots, lat, lon):
    d = {}
    d['lat'] = lat
    d['lon'] = lon
    es = Elasticsearch("http://ec2-52-3-61-194.compute-1.amazonaws.com:9200")
    INDEX_NAME = 'parktest'
    q = '{"query":{"filtered":{"query":{"match_all":{}},"filter":{"geo_distance":{"distance":"0.5km","location":{"lat":'+lat+',"lon":'+lon+'}}}}}}'
    result = es.search(index = INDEX_NAME, size=spots, body=q)
    lines = json.dumps(result['hits']['hits'])
    return lines

@app.route('/get_availability_hourly/<date>/<spot_name>')
def get_availability_hourly(date, spot_name):
        stmt = "SELECT * FROM hourly_location_aggregate WHERE event_time in (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) and spot_name=%s"
        response = session.execute(stmt, parameters=[date+'00' ,date+'01' ,date+'02' ,date+'03' ,date+'04' ,date+'05' ,date+'06' ,date+'07' ,date+'08' ,date+'09' ,date+'10' ,date+'11' , date+'12' ,date+'13' ,date+'14' ,date+'15' ,date+'16' ,date+'17' ,date+'18' ,date+'19' ,date+'20' ,date+'21' ,date+'22' ,date+'23', spot_name])

        response_list = []
        for val in response:
             response_list.append(val)
        jsonresponse = [{"timestamp": get_unix_epoch(x.event_time), "spot_name": x.spot_name, "Availability": x.availability} for x in response_list]
        return jsonify(result=jsonresponse)


def get_unix_epoch(time_stamp):
    time_struct = time.strptime(time_stamp, '%Y%m%d%H')
    return calendar.timegm(time_struct)


@app.route('/get_availability_daily/<date>')
def get_availability_daily(date):
        # print "date"
        stmt = "SELECT * FROM daily_location_aggregate WHERE event_time=%s"
        response = session.execute(stmt, parameters=[date])
        # print response
        response_list = []
        for val in response:
             response_list.append(val)
        jsonresponse = [{"timestamp": x.event_time, "spot_name": x.spot_name, "lat": x.lat, "lon": x.lon, "Availability": x.availability} for x in response_list]
        return jsonify(result=jsonresponse)


@app.route('/get_spot_names/')
def get_spot_names():
        date = '20150926'
        stmt = "SELECT spot_name FROM daily_location_aggregate WHERE event_time=%s"
        response = session.execute(stmt, parameters=[date])
        d = {}
        d['result'] = response
        return json.dumps(d)


@app.route("/save_parking_data", methods=['GET'])
def save_parking_data():
    firebase1 = firebase.FirebaseApplication('https://publicdata-parking.firebaseio.com', None)
    result = firebase1.get('/', None)
    with open('d2.txt', 'w') as f:
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
