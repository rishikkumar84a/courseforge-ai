import os
from motor.motor_asyncio import AsyncIOMotorClient
import urllib.parse

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DEFAULT_DB_NAME = "courseforge"

def get_database_name(uri: str, default_name: str) -> str:
    parsed_uri = urllib.parse.urlparse(uri)
    if parsed_uri.path and parsed_uri.path != "/":
        return parsed_uri.path.lstrip("/")
    return default_name

# A global client to be managed by application lifecycle hooks
db_client: AsyncIOMotorClient = None

async def connect_to_mongo():
    global db_client
    db_client = AsyncIOMotorClient(MONGODB_URI)

async def close_mongo_connection():
    global db_client
    if db_client:
        db_client.close()

async def get_db():
    global db_client
    db_name = get_database_name(MONGODB_URI, DEFAULT_DB_NAME)
    return db_client[db_name]
