from functools import lru_cache
import motor.motor_asyncio

from config import Settings

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()

client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URL)
db = client["imteste"]

users_collection = db.get_collection("users")
courses_collection = db.get_collection("courses")