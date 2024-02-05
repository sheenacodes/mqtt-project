#!/bin/sh

echo "Waiting for mqtt broker..."

while ! nc -z mqtt_broker 1883; do
  sleep 0.1
done

echo "mqtt broker started"

python publish.py
