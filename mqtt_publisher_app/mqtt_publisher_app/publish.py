import time
import paho.mqtt.client as mqtt
import os

# MQTT broker details
broker_address = os.getenv("MQTT_BROKER_ADDR", "localhost")
port = os.getenv("MQTT_BROKER_PORT", 1883)
topic = os.getenv("MQTT_TOPIC", "iot_1")


# Function to publish a message
def publish_message(client, message):
    client.publish(topic, message)
    print(f"Message published: {message}")


# MQTT callback when connection is established
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # Subscribe to the topic if needed
    # client.subscribe(topic)


def main():
    # Create MQTT client
    client = mqtt.Client()

    # Set callback functions
    client.on_connect = on_connect

    # Connect to the broker
    client.connect(broker_address, port, 60)

    # Start the loop
    client.loop_start()

    try:
        while True:
            # Your message to be sent
            message = "Hello, MQTT!"

            # Publish the message
            publish_message(client, message)

            # Wait for a minute
            time.sleep(10)

    except KeyboardInterrupt:
        print("Exiting...")

    finally:
        # Disconnect from the broker
        client.disconnect()
        client.loop_stop()


if __name__ == "__main__":
    main()
