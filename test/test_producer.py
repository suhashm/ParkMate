from kafka import SimpleProducer, KafkaClient
import json

# To send messages synchronously
kafka = KafkaClient('ec2-52-3-61-194.compute-1.amazonaws.com:9092')
producer = SimpleProducer(kafka)

def parking_data_producer(parking_json):
    producer.send_messages(b'test_steam_kafka', parking_json)

def main():
    d = {}
    # d['a'] = 'b'
    # d['c'] = 'd'
    d['m'] = 'n'
    d['o'] = 'p'
    e = json.dumps(d)
    ee = "hello how are you"
    parking_data_producer(ee)

if __name__ == "__main__":
    main()
