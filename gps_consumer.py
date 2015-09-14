from kafka import KafkaConsumer

# To consume messages
consumer = KafkaConsumer('gps',
                         group_id='my_group',
                         bootstrap_servers=['ec2-52-3-61-194.compute-1.amazonaws.com:9092'])
for message in consumer:
    # message value is raw byte string -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                         message.offset, message.key,
                                         message.value))
