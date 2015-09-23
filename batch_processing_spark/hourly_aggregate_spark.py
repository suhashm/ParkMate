"""Submit the program using ./bin/spark-submit --master spark://<Hostname>:7077 examples/a.py """

from pyspark import SparkContext, SparkConf
import json
import datetime

def write_to_cassandra(input):
    from cassandra.cluster import Cluster
    cluster = Cluster(['52.20.47.196'])
    session = cluster.connect('playground')
    stmt = "INSERT INTO test_hourly2 (event_time, garage_name, availability) VALUES (%s, %s,%s)"
    session.execute(stmt, parameters=[str(input[0][0]), input[0][1], str(input[1])])
    return input[0][1]

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
        res.append(((int(formatted_time), i.replace(" ","_").lower()), garages[i]['open_spaces']))
    return res

conf = SparkConf().setAppName("hourly-stats")
sc = SparkContext(conf=conf)
parking_json = sc.textFile("hdfs://ec2-52-3-61-194.compute-1.amazonaws.com:9000/camus/topics/park/hourly/2015/09/15/08/park.0.0.10.10.1442329200000.gz")
formatted_data = parking_json.flatMap(lambda s: create_tuple(s)).reduceByKey(lambda a,b: (int(a)+int(b))/2)
write_to_db = formatted_data.map(lambda line: write_to_cassandra(line))

print 'Total records', write_to_db.count()
