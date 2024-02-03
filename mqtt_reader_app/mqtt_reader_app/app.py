from fastapi import FastAPI
from pymongo import MongoClient
import os

# MongoDB Configuration
mongo_uri = os.getenv("MONGO_URI", "mongodb://admin:password@localhost:27017/")
database_name = os.getenv("MONDO_DB_NAME", "mqtt_messages")
collection_name = os.getenv("MONGO_COLLECTION_NAME", "messages")

# MongoDB Connection
mongo_client = MongoClient(mongo_uri)
db = mongo_client[database_name]
collection = db[collection_name]

app = FastAPI()


@app.get("/messages")
def get_messages():
    # Retrieve all messages from MongoDB
    messages = list(collection.find({}, {"_id": 0, "message": 1}))
    return {"messages": messages}


def main():
    import uvicorn

    # Run the FastAPI app using Uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
