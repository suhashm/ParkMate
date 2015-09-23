from kafka import SimpleProducer, KafkaClient
import random, json

# To send messages synchronously
kafka = KafkaClient('ec2-52-3-61-194.compute-1.amazonaws.com:9092')
producer = SimpleProducer(kafka)

# Data is of the format {userid, lat, lon}
def gps_data_producer():
    for i in range(10):
        d = {}
        d['userid'] = int(random.random() * 10000)
        d['lat'] = random.random()
        d['lon'] = random.random()
        coords = json.dumps(d)
        producer.send_messages(b'test-gps', coords)
