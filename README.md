# mqtt-project

    a monorepo of 3 services
    1)MQTT Publisher App: A service that publishes messages to an MQTT broker.
    2)MQTT Subscriber App: A service that subscribes to an MQTT topic, receives messages, and saves them to a MongoDB database.
    3)FastAPI App (MQTT Reader App): A FastAPI server exposing a RESTful API endpoint to retrieve messages saved in the MongoDB database.


## Table of Contents
- [Instruction](#instruction)
- [Instructions for Partially Local Set Up](#instructions-for-partially-local-set-up)


## Instruction

to set up broker, mongo-db and all the services
```bash
docker-compose up
```

- check it works at http://127.0.0.1:8000/messages
- check for message logs at mqtt_subscriber_app/log/

to run tests
```bash
docker-compose exec api python -m pytest .
docker-compose exe mqtt_subscriber python -m pytest .
```


## Instructions for Partially Local Set Up

to set up mqtt, at project root
```bash
docker-compose up mqtt_broker mongo_mqtt_store
```

to publish to mqtt
```bash
cd mqtt_publisher_app
poetry install
poetry run publish
```

to subscribe to published messages and save to db
```bash
cd mqtt_subscriber_app
poetry install
poetry run subscribe
```
to test:
```bash
poetry run pytest -o log_cli_level=DEBUG -s
```

to set up fastapi server to read messages from mongo db
```bash
cd mqtt_reader_app
poetry install
poetry run uvicorn-fastapi
```

check it works at http://127.0.0.1:8000/messages

to test:
```bash
poetry run pytest -o log_cli_level=DEBUG -s
```
