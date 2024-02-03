import paho.mqtt.client as mqtt
import os
from pymongo import MongoClient
import logging
import time
import sys

# Set up logging to a file
log_directory = "./log/"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Set up logging to a file
file_handler = logging.FileHandler(os.path.join(log_directory, "mqtt_messages.log"))
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)

# Create a logger for file logging
file_logger = logging.getLogger("file_logger")
file_logger.setLevel(logging.INFO)
file_logger.addHandler(file_handler)

# Set up logging to console
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)

# Create a logger for console logging
console_logger = logging.getLogger("console_logger")
console_logger.setLevel(logging.INFO)
console_logger.addHandler(console_handler)


# MQTT broker details
mqtt_broker_address = os.getenv("MQTT_BROKER_ADDR", "localhost")
mqtt_port = int(os.getenv("MQTT_BROKER_PORT", 1883))


MQTT_TOPIC_PREFIX = "charger/1/connector/1/session/"
topic = f"{MQTT_TOPIC_PREFIX}#"

# MongoDB Configuration
mongo_uri = os.getenv("MONGO_URI", "mongodb://admin:password@localhost:27017/")
database_name = os.getenv("MONDO_DB_NAME", "mqtt_messages")
collection_name = os.getenv("MONGO_COLLECTION_NAME", "messages")

# MongoDB Connection
mongo_client = MongoClient(mongo_uri)
db = mongo_client[database_name]
collection = db[collection_name]


def on_connect(client, userdata, flags, rc):
    """Callback function when connection is established to mqtt broker."""

    try:
        console_logger.info(f"Connected with result code {rc}")
        client.subscribe(topic)
    except Exception as e:
        console_logger.error(f"An error occurred while subscribing to the topic: {e}")


def on_message(client, userdata, message):
    """Callback function when a new message is received on a subscribed topic."""

    try:
        topic = message.topic
        payload = message.payload.decode("utf-8")
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        console_logger.info(
            f"Received message on topic {topic} at {timestamp}: {payload}"
        )

        payload = message.payload.decode("utf-8")
        file_logger.info(f"topic:{topic} timestamp:{timestamp} payload{payload}")

        # Save the message to MongoDB
        mongo_message = {"topic": topic, "payload": payload, "timestamp": timestamp}
        save_to_mongo(mongo_message)
    except Exception as e:
        console_logger.error(f"An error while processing received message: {e}")


def save_to_mongo(message):
    """Save the message in argument to MongoDB"""

    try:
        collection.insert_one({"message": message})
        console_logger.info("Message saved to MongoDB")
    except Exception as e:
        console_logger.error(f"An error occurred while saving message to MongoDB: {e}")


def main():
    try:
        # Create MQTT client
        mqtt_client = mqtt.Client()

        # Set callback functions
        mqtt_client.on_connect = on_connect
        mqtt_client.on_message = on_message

        # Connect to the broker
        mqtt_client.connect(mqtt_broker_address, mqtt_port, 60)

        # Start the loop
        mqtt_client.loop_forever()

    except KeyboardInterrupt:
        print("Exiting...")
    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        mqtt_client.disconnect()
        mqtt_client.loop_stop()


if __name__ == "__main__":
    main()
