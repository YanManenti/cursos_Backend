from typing import List, Optional
from bson import ObjectId
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.Database.database import PyObjectId


class InterestedContact(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "John Doe",
                "email": "jdoe@example.com"
            }
        }
    )


class Course(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str = Field(...)
    description: str = Field(...)
    price: float = Field(...)
    interested_list: List[InterestedContact] = []
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "Python for Beginners",
                "description": "A course for beginners in Python programming.",
                "price": 100.0,
                "interested_list": [
                    {
                        "name": "John Doe",
                        "email": "jdoe@example.com"
                    }
                ]
            }
        }
    )


class UpdateCourse(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    interested_list: Optional[List[InterestedContact]] = None
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "name": "Python for Beginners",
                "description": "A course for beginners in Python programming.",
                "price": 100.0,
                "interested_list": [
                    {
                        "name": "John Doe",
                        "email": "jdoe@example.com"
                    }
                ]
            }
        }
    )


class CourseCollection(BaseModel):
    courses: List[Course]
    