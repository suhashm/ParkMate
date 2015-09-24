"""Run using ./bin/spark-submit --packages org.apache.spark:spark-streaming-kafka_2.10:1.5.0 --master spark://<Hostname>:7077 examples/process_stream.py"""

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import json, datetime

def get_unix_time(ctime):
    time_list = ctime.split()
    # ctime 'Tue Sep 15 15:16:58 2015'

    # convert to ctime
    time_list = time_list[ :-2]

    temp = time_list[-1]
    time_list[-1] = time_list[-2]
    time_list[-2] = temp

    new_time = " ".join(time_list)
    b = datetime.datetime.strptime(new_time, "%a %b %d %H:%M:%S %Y")
    formatted_time = ""
    formatted_time += str(b.year)+str(b.month)+str(b.day)+str(b.hour)
    return formatted_time

def create_tuple(r):
    data = json.loads(r)
    res = []
    formatted_time = get_unix_time(data['san_francisco']['_updated'])
    garages = data['san_francisco']['garages']
    if '_geofire' in garages:
        garages.pop('_geofire')
    for i in garages:
        res.append(((int(formatted_time), i.replace(" ","_").lower(), garages[i]['points']), garages[i]['open_spaces']))

    streets = data['san_francisco']['streets']

    # remove geofire
    if '_geofire' in streets:
        streets.pop('_geofire')

    for i in streets:
        res.append(((int(formatted_time), i.replace(" ","_").lower()), streets[i]['open_spaces']))
        # streets[i]['open_spaces'] = random.randint(0,5)
        # streets[i]['points'] = streets[i]['points'][:2]

    return res

# Create a local StreamingContext with two working thread and batch interval of 5 second
sc = SparkContext("spark://ip-172-31-29-29:7077", "MyKafkaStream")
#ssc = StreamingContext(sc, 1)

# stream interval of 5 seconds
ssc = StreamingContext(sc, 5)
kafkaStream = KafkaUtils.createStream(ssc, "52.3.61.194:2181", "GroupNameDoesntMatter", {"parking_sensor_data": 2})
#messages = kafkaStream.map(lambda xs:xs)
messages = kafkaStream.flatMap(lambda s: create_tuple(s[1])).reduceByKey(lambda a,b: (int(a)+int(b))/2)
messages1 = messages.filter(lambda s: s[1] > 0)
#messages.print()
messages1.pprint()

ssc.start()             # Start the computation
ssc.awaitTermination()  # Wait for the computation to terminate
