from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.Database.database import PyObjectId
from app.Images.default import defaultUser

class User(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str = Field(...)
    email: EmailStr = Field(...)
    avatar: str = Field(default=defaultUser)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "John Doe",
                "email": "jdoe@example.com",
                "avatar": "839456ynq3...",
            }
        }
    )

class UserWithPassword(User):
    password: str = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "John Doe",
                "email": "jdoe@example.com",
                "avatar": "839456ynq3...",
                "password": "1234",
            }
        }
    )
     

class UpdateUser(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    avatar: Optional[str] = None
    password: Optional[str] = None
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "name": "John Doe",
                "email": "jdoe@example.com",
                "avatar": "839456ynq3...",
                "password": "1234",
            }
        }
    )


class UserCollection(BaseModel):
    users: List[User]