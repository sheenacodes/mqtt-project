import paho.mqtt.client as mqtt

broker_address = "localhost"
port = 1883
topic = "test_topic"


def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(topic)


def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()}")


if __name__ == "__main__":
    client = mqtt.Client()

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(broker_address, port, 60)

    client.loop_forever()
