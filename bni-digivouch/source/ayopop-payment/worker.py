from kafka import KafkaConsumer, KafkaProducer
import json, requests

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
        payload = json.loads(msg.value)
        bayar = requests.post('http://192.168.65.151:18082/v1/bill/payment', json=payload)
        print(bayar.text)