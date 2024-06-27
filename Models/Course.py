from typing import List, Optional
from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field


class Course(BaseModel):
    id: Optional[ObjectId] = Field(alias="_id", default=None)
    name: str = Field(...)
    description: str = Field(...)
    price: float = Field(...)
    is_active: bool = True
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=False,
        validate_all=True,
        json_schema_extra={
            "example": {
                "name": "Python for Beginners",
                "description": "A course for beginners in Python programming.",
                "price": 100.0,
                "is_active": True,
            }
        }
    )

class UpdateCourse(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    is_active: Optional[bool] = None
    model_config = ConfigDict(
        arbitrary_types_allowed=False,
        json_encoders={ObjectId: str},
        validate_all=True,
        json_schema_extra={
            "example": {
                "name": "Python for Beginners",
                "description": "A course for beginners in Python programming.",
                "price": 100.0,
                "is_active": True,
            }
        }
    )

class CourseCollection(BaseModel):
    courses: List[Course]
    