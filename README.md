# Project Name

The project is made as a simple data pipeline which contains:
- raw data in the form of csv/json files
- python script to pick up the raw data files and remove PII and load raw data tables in postgres
- dbt scripts to concatenate the raw data tables and load it to postgres

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)

## Installation

Instructions on how to install and set up the project.

```bash
docker-compose build
docker-compose up postgres
```

## Usage

to extract and load raw data

```bash
docker-compose run etl-service etl hb 2021-04-28
docker-compose run etl-service etl wwc 2021-04-28
docker-compose run etl-service etl wwc 2021-04-29
```

to concatenate tables and load.

```bash
docker-compose run dbt run --models concatenated_users
docker-compose run dbt test
```

to run the analytics queries
```bash
sh ./analytics/run_postgres_script.sh
```

##Tests
to run pytest

```bash
docker-compose run etl-service pytest
```
