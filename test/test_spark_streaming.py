"""Run using ./bin/spark-submit --packages org.apache.spark:spark-streaming-kafka_2.10:1.5.0 --master spark://<Hostname>:7077 examples/process_stream.py"""

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils


# Create a local StreamingContext with two working thread and batch interval of 2 second
sc = SparkContext("spark://ip-172-31-29-29:7077", "MyKafkaStream")
ssc = StreamingContext(sc, 1)

kafkaStream = KafkaUtils.createStream(ssc, "52.3.61.194:2181", "GroupNameDoesntMatter", {"test_steam_kafka": 2})

messages = kafkaStream.map(lambda xs:xs)
messages.pprint()

ssc.start()             # Start the computation
ssc.awaitTermination()  # Wait for the computation to terminate
