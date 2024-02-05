#!/bin/sh

echo "Waiting for mongo db..."

while ! nc -z mongo_mqtt_store 27017; do
  sleep 0.1
done

echo "mongo db started"

python app.py
