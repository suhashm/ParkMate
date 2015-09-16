from pyspark import SparkContext, SparkConf
import json
#import extract_time

import datetime
def get_unix_time(ctime):

    # convert ctime to unix timestamp
    time_list = ctime.split()
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
        #print i
        res.append(((formatted_time, i.replace(" ","_")), garages[i]['open_spaces']))
    return res

conf = SparkConf().setAppName("hourly-stats")
sc = SparkContext(conf=conf)
parking_json = sc.textFile("hdfs://ec2-52-3-61-194.compute-1.amazonaws.com:9000/camus/topics/park/hourly/2015/09/15/08/park.0.0.10.10.1442329200000.gz")
formatted_data = parking_json.flatMap(lambda s: create_tuple(s)).reduceByKey(lambda a,b: (int(a)+int(b))/2)
#formatted_data = parking_json.flatMap(lambda s: create_tuple(s))

print formatted_data.take(4)
