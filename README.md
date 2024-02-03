# mqtt-project

    mono repo of
    1) service that publish to a topic to mqtt broker
    2) service that subscribe to an mqtt topic and save it to a database
    3) restful api endpoint to retrieve the saved database messages


## Table of Contents

- [Installation](#installation)


- [Usage](#usage)

## Installation

to set up mqtt, at project root
```bash
docker-compose up
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

to set up fastapi server to read messages from mongo db
```bash
cd mqtt_reader_app
poetry install
poetry run uvicorn-fastapi
```
check it works at http://127.0.0.1:8000/messages
