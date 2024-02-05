#!/bin/sh

echo "Waiting for mqtt broker..."

while ! nc -z mqtt_broker 1883; do
  sleep 0.1
done

echo "mqtt broker started"

echo "Waiting for mongo db..."

while ! nc -z mongo_mqtt_store 27017; do
  sleep 0.1
done

echo "mongo db started"

python mqtt_subscriber_app/subscribe.py
