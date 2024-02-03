from unittest.mock import patch, Mock
from mqtt_subscriber_app.subscribe import (
    on_connect,
    on_message,
    save_to_mongo,
)

# mqtt topic and payload
TEST_TOPIC = "charger/1/connector/1/session/#"
TEST_PAYLOAD = "Test payload"


def test_on_connect():
    """Test on_connect function - that topic is subscibed to"""

    # Create a mock client object and call on_connect with it
    mock_client = Mock()
    on_connect(mock_client, None, None, None)

    # Check if subscribe is called with the correct topic
    mock_client.subscribe.assert_called_once_with(TEST_TOPIC)


def test_on_message():
    """Test on_message function - that the message is logged and saved to MongoDB"""

    # Create a mock message object
    mock_message = Mock()
    mock_message.topic = TEST_TOPIC
    mock_message.payload.decode.return_value = TEST_PAYLOAD

    # Create mock loggers and patch the on_message function to use them
    with patch(
        "mqtt_subscriber_app.subscribe.file_logger", autospec=True
    ) as mock_file_logger, patch(
        "mqtt_subscriber_app.subscribe.save_to_mongo", autospec=True
    ) as mock_save_to_mongo, patch(
        "mqtt_subscriber_app.subscribe.time", autospec=True
    ) as mock_time:
        # Set the return value for time.strftime to a fixed value
        mock_time.strftime.return_value = "MOCKED_TIMESTAMP"

        on_message(None, None, mock_message)

        # Check if file_logger.info is called with the correct arguments
        mock_file_logger.info.assert_called_once_with(
            f"topic:{TEST_TOPIC} timestamp:MOCKED_TIMESTAMP payload{TEST_PAYLOAD}"
        )

        # Check if save_to_mongo is called with the correct arguments
        mock_save_to_mongo.assert_called_once_with(
            {
                "topic": TEST_TOPIC,
                "payload": TEST_PAYLOAD,
                "timestamp": "MOCKED_TIMESTAMP",
            }
        )


def test_save_to_mongo():
    """Test save_to_mongo function - that the message is saved to MongoDB."""

    # Create a mock collection object
    mock_collection = Mock()

    # Patch the collection object in the script
    with patch("mqtt_subscriber_app.subscribe.collection", mock_collection):
        # Call save_to_mongo with a mock message
        save_to_mongo(
            {
                "topic": TEST_TOPIC,
                "payload": TEST_PAYLOAD,
                "timestamp": "MOCKED_TIMESTAMP",
            }
        )

        # Check if insert_one is called with the correct argument
        mock_collection.insert_one.assert_called_once_with(
            {
                "message": {
                    "topic": TEST_TOPIC,
                    "payload": TEST_PAYLOAD,
                    "timestamp": "MOCKED_TIMESTAMP",
                }
            }
        )
