import paho.mqtt.client as mqtt
import os

# MQTT broker details
broker_address = os.getenv("MQTT_BROKER_ADDR", "localhost")
port = os.getenv("MQTT_BROKER_PORT", 1883)
topic = os.getenv("MQTT_TOPIC", "iot_1")


def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(topic)


def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()}")


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

    finally:
        client.disconnect()
        client.loop_stop()


if __name__ == "__main__":
    main()
