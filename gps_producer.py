from kafka import SimpleProducer, KafkaClient
import random, json

# To send messages synchronously
kafka = KafkaClient('ec2-52-3-61-194.compute-1.amazonaws.com:9092')
producer = SimpleProducer(kafka)

def gps_data_producer():
    for i in range(10):
        d = {}
        d['lat'] = random.random()
        d['lon'] = random.random()
        coords = json.dumps(d)
        producer.send_messages(b'gps', coords)
