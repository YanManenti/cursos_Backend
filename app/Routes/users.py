import hashlib
from http import HTTPStatus
from bson import ObjectId
from fastapi import APIRouter, Body, Form, HTTPException
from pymongo import ReturnDocument

from app.Database.database import users_collection
from app.Models.User import UpdateUser, User, UserCollection, UserWithPassword
from app.Images.default import defaultUser

router = APIRouter(
    prefix="/api/users",
    tags=["users"],
)

# Login route
@router.post("/login",
             response_model=User,
             response_model_by_alias=False)
async def login(email: str = Form(...), password: str = Form(...)):
    password = hashlib.sha256(password.encode()).hexdigest()
    user = await users_collection.find_one({"email": email, "password": password})
    if(user is None):
        return HTTPException(status_code=404, detail="User not found")
    
    return user


# Gets all users from the database and returns them as a list
@router.get("/",
            response_model=UserCollection,
            response_model_by_alias=False
            )
async def read_all_users():

    data = []
    cursor = users_collection.find()

    for document in await cursor.to_list(length=10):
        data.append(document)

    return UserCollection(users=data)


# Gets a user by their Id
@router.get("/{user_id}",
            response_model=User,
            response_model_by_alias=False
            )
async def read_user(user_id: str):

    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if(user is None):
        return HTTPException(status_code=404, detail="User not found")
    
    return user


# Creates a new user
@router.post("/",
             response_model=User,
             status_code=HTTPStatus.CREATED,
             response_model_by_alias=False
             )
async def create_user(user: UserWithPassword = Body(...)):

    user.password = hashlib.sha256(user.password.encode()).hexdigest()

    if(user.avatar == "" or user.avatar is None):
        user.avatar = defaultUser

    newUser = await users_collection.insert_one(user.model_dump(by_alias=True, exclude=["id"]))
    if(newUser is None):
        return HTTPException(status_code=404, detail="Error creating user")
    
    createdUser = await users_collection.find_one({"_id": newUser.inserted_id})
    if(createdUser is None):
        return HTTPException(status_code=404, detail="Error finding created user")
    
    return createdUser


# Updates a user by their Id
@router.put("/{user_id}",
            response_model=User,
            response_model_by_alias=False)
async def update_user(user_id: str, user: UpdateUser = Body(...)):

    # Iterates through the received user dictionary and removes any None values
    user={
        key: value for key, value in user.model_dump(by_alias=True).items() if value is not None
    }

    if("password" in user):
        user["password"] = hashlib.sha256(user["password"].encode()).hexdigest()

    updatedUser = await users_collection.find_one_and_update({"_id": ObjectId(user_id)}, {"$set": user}, return_document=ReturnDocument.AFTER)
    if(updatedUser is None):
        return HTTPException(status_code=404, detail=f"User {user_id} not found")
    
    updatedUser = await users_collection.find_one({"_id": ObjectId(user_id)})
    if(updatedUser is None):
        return HTTPException(status_code=404, detail=f"User {user_id} not found after update")
    
    return updatedUser


# Deletes a user by their Id
@router.delete("/{user_id}")
async def delete_user(user_id: str):

    deleteResult = await users_collection.delete_one({"_id": ObjectId(user_id)})
    if(deleteResult.deleted_count == 0):
        return HTTPException(status_code=404, detail=f"User {user_id} not found")
    
    return {"detail": f"{deleteResult.deleted_count} user(s) deleted"}
