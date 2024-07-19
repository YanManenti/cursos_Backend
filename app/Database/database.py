from functools import lru_cache
import os
from typing import Annotated
import motor.motor_asyncio
from pydantic import BeforeValidator

# from app.config import Settings

PyObjectId = Annotated[str, BeforeValidator(str)]


# @lru_cache
# def get_settings():
#     return Settings()

# settings = get_settings()

# client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGODB_URL"))
# client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URL)
client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://mongoadmin:secret@localhost:27017/")
db = client["imteste"]


users_collection = db.get_collection("users")
courses_collection = db.get_collection("courses")