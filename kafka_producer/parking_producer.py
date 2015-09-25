from kafka import SimpleProducer, KafkaClient

# To send messages synchronously
kafka = KafkaClient('ec2-52-3-61-194.compute-1.amazonaws.com:9092')
producer = SimpleProducer(kafka)

def parking_data_producer(parking_json):
    # Note that the application is responsible for encoding messages to type bytes
    # producer.send_messages(b'test-park', parking_json)
    producer.send_messages(b'parking_sensor_topic', parking_json)
