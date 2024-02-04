from fastapi import FastAPI, Depends
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


# Dependency to get MongoDB client
def get_mongo_client():
    return MongoClient(mongo_uri)


# Dependency to get MongoDB database
def get_database(client: MongoClient = Depends(get_mongo_client)):
    return client[database_name]


# Dependency to get MongoDB collection
def get_collection(db=Depends(get_database)):
    return db[collection_name]


# FastAPI route using the dependencies
@app.get("/messages")
async def get_messages(collection=Depends(get_collection)):
    messages = list(collection.find({}, {"_id": 0, "message": 1}))
    return {"messages": messages}


def main():
    import uvicorn

    # Run the FastAPI app using Uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
