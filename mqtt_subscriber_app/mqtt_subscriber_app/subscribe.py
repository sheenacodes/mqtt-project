import paho.mqtt.client as mqtt
import os
from pymongo import MongoClient
import logging
import time
import sys
from pydantic_settings import BaseSettings


# configuration from environment variables
class Settings(BaseSettings):
    mongo_uri: str = "mongodb://admin:password@localhost:27017/"
    mongo_db_name: str = "mqtt_messages"
    mongo_collection_name: str = "messages"
    mqtt_broker_addr: str = "localhost"
    mqtt_port: int = 1883
    log_level: str = "INFO"


settings = Settings()

# Set up logging to a file
log_directory = "./log/"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Set up logging to a file
file_handler = logging.FileHandler(os.path.join(log_directory, "mqtt_messages.log"))
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)

# Create a logger for file logging
file_logger = logging.getLogger("file_logger")
file_logger.setLevel(logging.INFO)
file_logger.addHandler(file_handler)

# Set up logging to console
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)

# Create a logger for console logging
console_logger = logging.getLogger("console_logger")
console_logger.setLevel(settings.log_level.upper())
console_logger.addHandler(console_handler)


MQTT_TOPIC_PREFIX = "charger/1/connector/1/session/"
topic = f"{MQTT_TOPIC_PREFIX}#"

# MongoDB Connection
mongo_client = MongoClient(settings.mongo_uri)
db = mongo_client[settings.mongo_db_name]
collection = db[settings.mongo_collection_name]


def on_connect(client, userdata, flags, rc):
    """Callback function when connection is established to mqtt broker."""

    try:
        console_logger.info(f"Connected with result code {rc}")
        client.subscribe(topic)
    except Exception as e:
        console_logger.error(f"An error occurred while subscribing to the topic: {e}")
        raise


def on_message(client, userdata, message):
    """Callback function when a new message is received on a subscribed topic."""

    try:
        topic = message.topic
        payload = message.payload.decode("utf-8")
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        console_logger.debug(
            f"Received message on topic {topic} at {timestamp}: {payload}"
        )

        payload = message.payload.decode("utf-8")

        # Log the message to a file
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
        mqtt_client.connect(settings.mqtt_broker_addr, settings.mqtt_port, 60)

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
