from kafka.client import KafkaClient
from kafka.consumer import SimpleConsumer
from kafka.producer import SimpleProducer
client = KafkaClient("ec2-52-3-61-194.compute-1.amazonaws.com:9092")
consumer = SimpleConsumer(client, "test-group", "gps")

for message in consumer:
        print(message)
