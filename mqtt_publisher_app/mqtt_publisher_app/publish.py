import time
import paho.mqtt.client as mqtt
import os
import logging
import random
import json

# set logging level
logging.basicConfig(level=logging.INFO)

# MQTT broker details
broker_address = os.getenv("MQTT_BROKER_ADDR", "localhost")
port = int(os.getenv("MQTT_BROKER_PORT", 1883))
MQTT_TOPIC_PREFIX = "charger/1/connector/1/session/"


def on_connect(client, userdata, flags, rc):
    logging.info(f"Connected with result code {rc}")


def on_publish(client, userdata, mid):
    logging.info(f"Message {mid} published")


def main():
    client = mqtt.Client()

    client.connect(broker_address, port, 60)
    client.loop_start()

    try:
        session_id = 1
        while True:
            message = {
                "session_id": session_id,
                "energy_delivered_in_kWh": random.randint(1, 70),
                "duration_in_seconds": random.randint(10, 100),
                "session_cost_in_cents": random.randint(30, 100),
            }
            topic = f"{MQTT_TOPIC_PREFIX}{session_id}"
            client.publish(topic, json.dumps(message))
            logging.info(f"Message published: {message}")
            time.sleep(60)
            session_id += 1

    except KeyboardInterrupt:
        print("Exiting...")

    finally:
        client.disconnect()
        client.loop_stop()


if __name__ == "__main__":
    main()
