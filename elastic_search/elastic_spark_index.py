"""Run using ./bin/spark-submit --packages org.apache.spark:spark-streaming-kafka_2.10:1.5.0 --master spark://<Hostname>:7077 examples/process_stream.py"""
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import json, datetime, os
#import index_cluster
from elasticsearch import Elasticsearch

def create_index(data):
# connect to the elasticsearch instance
    es = Elasticsearch("http://ec2-52-3-61-194.compute-1.amazonaws.com:9200")

    # create index and mapping
    INDEX_NAME = 'parktest'
    if not es.indices.exists(INDEX_NAME):
        print("deleting index...")
        #res = es.indices.delete(index = INDEX_NAME)

        os.system('curl -X PUT ec2-52-3-61-194.compute-1.amazonaws.com:9200/parktest/')

        bb= """curl -X PUT ec2-52-3-61-194.compute-1.amazonaws.com:9200/parktest/parktest/_mapping -d '{
            "parktest": {
                "properties": {
                    "location": {
                        "type": "geo_point",
                        "lat_lon": true,
                        "geohash": true
                    }
                }
            }
        }'
        """
        os.system(bb)
        # q = '{"query":{"filtered":{"query":{"match_all":{}},"filter":{"geo_distance":{"distance":"100km","location":{"lat":46.884106,"lon":-71.377042}}}}}}'
        # q = '{"query":{"match_all":{}},"script_fields":{"distance":{"params":{"lat":46.884106,"lon":-71.377042},"script":"doc[\u0027location\u0027].distanceInKm(lat,lon)"}},"filter":{"geo_distance":{"distance":"100km","location":{"lat":46.884106,"lon":-71.377042}}}}'
        # q = '{"query":{"filtered":{"query":{"match_all":{}},"filter":{"geo_distance":{"distance":"100km","location":{"lat":12.969773,"lon":77.597337}}}}}}'
        # results = helpers.bulk(es, bulk_data1, index='geotest', doc_type='geotest', refresh=True)
        # results = helpers.bulk(es, bulk_data1, index=INDEX_NAME, doc_type=INDEX_NAME, refresh=True)
        d = {}
        d['time'] = data[0][0]
        d['garage_name'] = data[0][1]
        location = {}
        location['lat'] = data[0][2]
        location['lon'] = data[0][3]
        d['location'] = location
        d['availability'] = data[1]
        es.index(index=INDEX_NAME, doc_type=INDEX_NAME, body=d, refresh=True)

def get_unix_time(ctime):
    time_list = ctime.split()
    # ctime 'Tue Sep 15 15:16:58 2015'

    # convert to ctime - this is for hourly analysis and hence ignoring
    time_list = time_list[ :-2]

    temp = time_list[-1]
    time_list[-1] = time_list[-2]
    time_list[-2] = temp

    new_time = " ".join(time_list)
    b = datetime.datetime.strptime(new_time, "%a %b %d %H:%M:%S %Y")
    formatted_time = ""
    formatted_time += str(b.year)+str(b.month)+str(b.day)+str(b.hour)
    return formatted_time

# create tuple of the format((timestamp, name, lat, lon), availability)
def create_tuple(r):
    data = json.loads(r)
    res = []
    formatted_time = get_unix_time(data['san_francisco']['_updated'])
    garages = data['san_francisco']['garages']
    if '_geofire' in garages:
        garages.pop('_geofire')
    for i in garages:
        res.append(((int(formatted_time), i.replace(" ","_").lower(), garages[i]['points'][0],garages[i]['points'][1]), garages[i]['open_spaces']))

    streets = data['san_francisco']['streets']

    # remove geofire
    if '_geofire' in streets:
        streets.pop('_geofire')

    for i in streets:
        res.append(((int(formatted_time), i.replace(" ","_").lower(), streets[i]['points'][0], streets[i]['points'][1]), streets[i]['open_spaces']))

    return res

# Create a local StreamingContext with two working thread and batch interval of 5 second
sc = SparkContext("spark://ip-172-31-29-29:7077", "MyKafkaStream")
#ssc = StreamingContext(sc, 1)

# stream interval of 5 seconds
ssc = StreamingContext(sc, 5)
kafkaStream = KafkaUtils.createStream(ssc, "52.3.61.194:2181", "GroupNameDoesntMatter", {"parking_sensor_data": 2})
kafkaStream.repartition(50)
#messages1 = kafkaStream.map(lambda xs:xs)
messages = kafkaStream.flatMap(lambda s: create_tuple(s[1])).reduceByKey(lambda a,b: (int(a)+int(b))/2)
messages1 = messages.filter(lambda s: s[1] > 0)
#messages.print()
m2 =messages1.map(lambda s: create_index(s))
#m2 = messages1.map(lambda s: s)
messages1.pprint()

ssc.start()             # Start the computation
ssc.awaitTermination()  # Wait for the computation to terminate
