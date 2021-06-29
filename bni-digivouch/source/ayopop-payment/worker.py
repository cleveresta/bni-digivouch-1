from kafka import KafkaConsumer
import json

if __name__ == "__main__":
    consumer = KafkaConsumer(
        "ayopop-payment",
        bootstrap_servers='localhost:9092',
        auto_offset_reset='latest',
        group_id="consumer-group-a",
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
    print("starting the consumer")
    for msg in consumer:
        print("payment ayopop = {}".format(msg.value))