# test_app.py
import pytest
from pymongo import MongoClient
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from mqtt_reader_app.app import app, get_collection, get_database, get_mongo_client

# MongoDB Configuration for testing
test_mongo_uri = "mongodb://admin:password@localhost:27017/"
test_database_name = "test_mqtt_messages"  # Use a different database for testing
test_collection_name = "test_messages"


# Pytest fixture to create and populate the test database
@pytest.fixture
def test_database():
    # Assuming you're using MongoClient, create the test database
    test_client = MongoClient(test_mongo_uri)
    test_db = test_client[test_database_name]

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
    test_db[test_collection_name].insert_many(test_data)

    yield test_db  # Provide the test database as a fixture

    # Teardown: Drop the test database after the test
    test_client.drop_database(test_database_name)

    print(f"Dropped Test Database: {test_database_name}")


# Override the MongoDB connection in the FastAPI app for testing
def override_dependencies(test_database):
    app.dependency_overrides[get_mongo_client] = lambda: MagicMock()
    app.dependency_overrides[get_database] = lambda: test_database
    app.dependency_overrides[get_collection] = lambda: test_database[
        test_collection_name
    ]

    print(f"Overriding dependencies with Test Database: {test_database}")


# Test function to check if /messages returns correct response
def test_get_messages(test_database):
    print(f"Test Database: {test_database}")
    print(f"Test Data: {test_database[test_collection_name].find_one()}")
    # Override dependencies
    override_dependencies(test_database)

    # Create a test client
    client = TestClient(app)

    # Make a request to the /messages endpoint
    response = client.get("/messages")

    # Check if the response status code is 200 (OK)
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


# Test function to check if the main function runs without errors
def test_main_function():
    # Override dependencies
    override_dependencies(MagicMock())

    # Mock the uvicorn.run function
    with patch("uvicorn.run") as mock_run:
        # Call the main function
        from mqtt_reader_app.app import main

        main()

        # Ensure uvicorn.run was called with the expected arguments
        mock_run.assert_called_once_with(app, host="127.0.0.1", port=8000)
