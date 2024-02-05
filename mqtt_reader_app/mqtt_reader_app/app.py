from fastapi import FastAPI, Depends
from pymongo import MongoClient
import logging
from pydantic_settings import BaseSettings


# mongo db configuration
class Settings(BaseSettings):
    mongo_uri: str = "mongodb://admin:password@localhost:27017/"
    mongo_db_name: str = "mqtt_messages"
    mongo_collection_name: str = "messages"
    log_level: str = "INFO"


settings = Settings()

logging.basicConfig(level=settings.log_level.upper())

# MongoDB Connection
mongo_client = MongoClient(settings.mongo_uri)
db = mongo_client[settings.mongo_db_name]
collection = db[settings.mongo_collection_name]

app = FastAPI()


# Dependency to get MongoDB client
def get_mongo_client():
    return MongoClient(settings.mongo_uri)


# Dependency to get MongoDB database
def get_database(client: MongoClient = Depends(get_mongo_client)):
    return client[settings.mongo_db_name]


# Dependency to get MongoDB collection
def get_collection(db=Depends(get_database)):
    return db[settings.mongo_collection_name]


# route using the dependencies
@app.get("/messages")
async def get_messages(collection=Depends(get_collection)):
    messages = list(collection.find({}, {"_id": 0, "message": 1}))
    logging.debug("/messages called")
    return {"messages": messages}


def main():
    import uvicorn

    # Run the FastAPI app using Uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
