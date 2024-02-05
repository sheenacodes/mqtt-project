# test_app.py
import pytest
from pymongo import MongoClient
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from mqtt_reader_app.app import app, get_collection, get_database, get_mongo_client
from pydantic_settings import BaseSettings


# mongo db configuration
class Settings(BaseSettings):
    test_mongo_uri: str = "mongodb://admin:password@localhost:27017/"
    test_mongo_db_name: str = "test_mqtt_messages"
    test_mongo_collection_name: str = "test_messages"


settings = Settings()


@pytest.fixture
def test_database():
    """Create a test database and insert test data. Provide the test database as a fixture."""

    # create the test database
    test_client = MongoClient(settings.test_mongo_uri)
    test_db = test_client[settings.test_mongo_db_name]

    # Insert test data into the test collection
    test_data = [
        {
            "message": {
                "topic": "test/topic1",
                "payload": "Test payload 1",
                "timestamp": "2024-02-04 01:01:27",
            }
        }
    ]
    test_db[settings.test_mongo_collection_name].insert_many(test_data)

    # Provide the test database as a fixture
    yield test_db

    # Teardown: Drop the test database after the test
    test_client.drop_database(settings.test_mongo_db_name)


def override_dependencies(test_database):
    """Override the MongoDB dependencies in the FastAPI app with the test database."""
    app.dependency_overrides[get_mongo_client] = lambda: MagicMock()
    app.dependency_overrides[get_database] = lambda: test_database
    app.dependency_overrides[get_collection] = lambda: test_database[
        settings.test_mongo_collection_name
    ]

    print(f"Overriding dependencies with Test Database: {test_database}")


def test_get_messages(test_database):
    """Test the /messages route of the FastAPI app."""

    # Override the MongoDB connection in the FastAPI app and send a request using the TestClient
    override_dependencies(test_database)
    client = TestClient(app)
    response = client.get("/messages")
    assert response.status_code == 200

    # Check if the response contains the expected test data
    assert response.json() == {
        "messages": [
            {
                "message": {
                    "topic": "test/topic1",
                    "payload": "Test payload 1",
                    "timestamp": "2024-02-04 01:01:27",
                }
            }
        ]
    }


def test_main_function():
    """Test the main function of the FastAPI app."""

    # Mock the uvicorn.run function
    with patch("uvicorn.run") as mock_run:
        from mqtt_reader_app.app import main

        # Call the main function and ensure that uvicorn.run is called with the correct arguments
        main()
        mock_run.assert_called_once_with(app, host="0.0.0.0", port=8000)
