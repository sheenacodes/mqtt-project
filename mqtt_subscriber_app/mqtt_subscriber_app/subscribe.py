import paho.mqtt.client as mqtt
import os
from pymongo import MongoClient

# MQTT broker details
broker_address = os.getenv("MQTT_BROKER_ADDR", "localhost")
port = os.getenv("MQTT_BROKER_PORT", 1883)
topic = os.getenv("MQTT_TOPIC", "iot_1")

# MongoDB Configuration
mongo_uri = os.getenv("MONGO_URI", "mongodb://admin:password@localhost:27017/")
database_name = os.getenv("MONDO_DB_NAME", "mqtt_messages")
collection_name = os.getenv("MONGO_COLLECTION_NAME", "messages")

# MongoDB Connection
mongo_client = MongoClient(mongo_uri)
db = mongo_client[database_name]
collection = db[collection_name]


def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(topic)


def on_message(client, userdata, message):
    # Callback function when a new message is received
    payload = message.payload.decode("utf-8")
    print(f"Received message: {payload}")

    # Save the message to MongoDB
    save_to_mongo(payload)


def save_to_mongo(message):
    # Insert the message into the MongoDB collection
    collection.insert_one({"message": message})
    print("Message saved to MongoDB")


def main():
    try:
        # Create MQTT client
        client = mqtt.Client()

        # Set callback functions
        client.on_connect = on_connect
        client.on_message = on_message

        # Connect to the broker
        client.connect(broker_address, port, 60)

        # Start the loop
        client.loop_forever()

    except KeyboardInterrupt:
        print("Exiting...")
    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        client.disconnect()
        client.loop_stop()


if __name__ == "__main__":
    main()
