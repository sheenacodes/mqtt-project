import time
import paho.mqtt.client as mqtt
import os

# MQTT broker details
broker_address = os.getenv("MQTT_BROKER_ADDR", "localhost")
port = os.getenv("MQTT_BROKER_PORT", 1883)
topic = os.getenv("MQTT_TOPIC", "iot_1")


def main():
    client = mqtt.Client()

    client.connect(broker_address, port, 60)
    client.loop_start()

    try:
        while True:
            message = "Hello, MQTT!"
            client.publish(topic, message)
            print(f"Message published: {message}")
            time.sleep(5)

    except KeyboardInterrupt:
        print("Exiting...")

    finally:
        client.disconnect()
        client.loop_stop()


if __name__ == "__main__":
    main()
