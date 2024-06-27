from typing import Annotated, List, Optional

from bson import ObjectId
from pydantic import BaseModel, BeforeValidator, ConfigDict, EmailStr, Field

PyObjectId = Annotated[str, BeforeValidator(str)]


class User(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "John Doe",
                "email": "jdoe@example.com",
                "password": "031edd7d41651593c5fe5c006fa5752b37fddff7bc4e843aa6af0c950f4b9406",
            }
        }
    )
     
class UpdateUser(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "name": "John Doe",
                "email": "jdoe@example.com",
                "password": "031edd7d41651593c5fe5c006fa5752b37fddff7bc4e843aa6af0c950f4b9406",
            }
        }
    )

class UserCollection(BaseModel):
    users: List[User]