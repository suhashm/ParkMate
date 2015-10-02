"""Submit the program using /usr/local/spark/bin/spark-submit --packages TargetHolding/pyspark-cassandra:0.1.5 --conf spark.cassandra.connection.host=<Private IP - a.b.c.d> --master spark://<Hostname - ip-a-b-c-d>:7077 ~/spark_batch_processing/average_hourly_availability_spark.py """

from pyspark import SparkContext, SparkConf
import json

def write_to_cassandra(input):
    """write the input to cassandra """
    from cassandra.cluster import Cluster
    cluster = Cluster(['52.20.47.196'])
    session = cluster.connect('parking')
    stmt = "INSERT INTO hourly_aggregate (event_time, spot_name, availability) VALUES (%s, %s,%s)"
    session.execute(stmt, parameters=[str(input[0][0]), input[0][1], str(input[1])])
    return input[0][1]


def get_unix_time_hourly(ctime):
    """get YYYMMDD information from a given date"""
    time_list = ctime.split('-')
    return time_list[0]


def create_tuple(r):
    """create tuple of the form ((timestamp, parking_spot_name), availability)"""
    data = json.loads(r)
    res = []
    formatted_time = get_unix_time_hourly(data['san_francisco']['_updated'])
    garages = data['san_francisco']['garages']
    if '_geofire' in garages:
        garages.pop('_geofire')
    for i in garages:
        # add lat lon information to tuple
        res.append(((int(formatted_time), i.replace(" ","_").lower(), garages[i]['points'][0], garages[i]['points'][1]), garages[i]['open_spaces']))

    streets = data['san_francisco']['streets']

    # remove geofire
    if '_geofire' in streets:
        streets.pop('_geofire')

    for i in streets:
        if streets[i]['open_spaces'] != 'Unknown':
            res.append(((int(formatted_time), i.replace(" ","_").lower(), streets[i]['points'][0], streets[i]['points'][1]), streets[i]['open_spaces']))
        else:
            res.append(((int(formatted_time), i.replace(" ","_").lower(), streets[i]['points'][0], streets[i]['points'][1]), 4))

    return res

def main():
    conf = SparkConf().setAppName("average_parking_availability_daily")
    sc = SparkContext(conf=conf)

    # read data from HDFS
    parking_json = sc.textFile("hdfs://ec2-52-3-61-194.compute-1.amazonaws.com:9000/user/parking_data/history/hdfs_parking_sensor_topic_20150928185*",150)

    # get the average availability for a parking spot
    formatted_data = parking_json.flatMap(lambda s: create_tuple(s)).filter(lambda s: str(s[1]) !='Unknown').reduceByKey(lambda a,b: (int(a)+int(b))/2)

    # convert it to cassandra hourly average schema type (event_time, spot_name, availability, lat, lon)
    to_db = formatted_data.map(lambda s: (s[0][0],s[0][1], str(s[1]), str(s[0][2]), str(s[0][3])))

    to_db = to_db.filter(lambda s: s[4] != 'Unknown')

    # write the data to cassandra
    to_db.saveToCassandra("parking", "daily_location_aggregate",) # save RDD to cassandra

    print to_db.take(10)

if __name__ == '__main__':
    main()


