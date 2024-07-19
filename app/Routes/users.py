import hashlib
from http import HTTPStatus
import re
from bson import ObjectId
from fastapi import APIRouter, Body, Depends, Form, HTTPException, Security
from pymongo import ReturnDocument

from app.Database.database import users_collection
from app.Models.User import UpdateUser, User, UserCollection, UserWithPassword
from app.Images.default import defaultUser

# from Database.database import users_collection
# from Models.User import UpdateUser, User, UserCollection, UserWithPassword
# from Images.default import defaultUser

from fastapi_jwt import (
    JwtAccessBearerCookie,
    JwtAuthorizationCredentials,
    JwtRefreshBearer,
)
from datetime import timedelta



router = APIRouter(
    prefix="/api/users",
    tags=["users"],
)

# Read access token from bearer header and cookie (bearer priority)
access_security = JwtAccessBearerCookie(
    secret_key="secret_key",
    auto_error=True,
    access_expires_delta=timedelta(hours=24)  # change access token validation timedelta
)
# Read refresh token from bearer header only
refresh_security = JwtRefreshBearer(
    secret_key="secret_key", 
    auto_error=True  # automatically raise HTTPException: HTTP_401_UNAUTHORIZED 
)

# Login route
@router.post("/login",
             response_model_by_alias=False)
async def login(email: str = Body(...), password: str = Body(...)):
    passwordRegex = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
    emailRegex = r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
    if(not re.match(emailRegex, email)):
        raise HTTPException(status_code=400, detail="Email inválido")
    if(not re.match(passwordRegex, password)):
        raise HTTPException(status_code=400, detail="Senha inválida")

    password = hashlib.sha256(password.encode()).hexdigest()
    user = await users_collection.find_one({"email": email, "password": password})
    if(user is None):
        raise HTTPException(status_code=404, detail="User not found")
    
    subject = {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
    }

    # Create new access/refresh tokens pair
    access_token = access_security.create_access_token(subject=subject)
    refresh_token = refresh_security.create_refresh_token(subject=subject)

    return {"access_token": access_token, "refresh_token": refresh_token}


# Logout route
@router.post("/logout")
def logout(refresh_token: str = Form(...)):
    # Blacklist refresh token
    refresh_security.revoke_refresh_token(refresh_token)
    return {"detail": "Logout successful"}


# Refresh route to get new access token
@router.post('/refresh')
def refresh(
        credentials: JwtAuthorizationCredentials = Security(refresh_security)
):
    
    access_token = access_security.create_access_token(subject=credentials.subject)
    refresh_token = refresh_security.create_refresh_token(subject=credentials.subject, expires_delta=timedelta(days=2))

    return {"access_token": access_token, "refresh_token": refresh_token}


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
@router.get("/avatar/{user_id}",
            response_model_by_alias=False
            )
async def read_user(user_id: str):

    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if(user is None):
        raise HTTPException(status_code=404, detail="User not found")

    # now we can access Credentials object
    return {"avatar": user["avatar"]}

# Gets the user based on the access token
@router.get("/me",
            response_model_by_alias=False
            )
async def read_user(credentials: JwtAuthorizationCredentials = Security(access_security)):
    id = credentials["id"]
    user = await users_collection.find_one({"_id": ObjectId(id)})
    if(user is None):
        raise HTTPException(status_code=404, detail="User not found")
    
    subject = {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
    }

    return {"subject": subject}

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
    
    sameNameUser = await users_collection.find_one({"name": user.name})
    if(sameNameUser is not None):
        raise HTTPException(status_code=400, detail="Usuário com este nome já existe")
    
    sameEmailUser = await users_collection.find_one({"email": user.email})
    if(sameEmailUser is not None):
        raise HTTPException(status_code=400, detail="Usuário com este email já existe")

    newUser = await users_collection.insert_one(user.model_dump(by_alias=True, exclude=["id"]))
    if(newUser is None):
        raise HTTPException(status_code=500, detail="Erro ao criar usuário")
    
    createdUser = await users_collection.find_one({"_id": newUser.inserted_id})
    if(createdUser is None):
        raise HTTPException(status_code=500, detail="Erro ao encontrar usuário criado")
    
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
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    
    updatedUser = await users_collection.find_one({"_id": ObjectId(user_id)})
    if(updatedUser is None):
        raise HTTPException(status_code=404, detail=f"User {user_id} not found after update")
    
    return updatedUser


# Deletes a user by their Id
@router.delete("/{user_id}")
async def delete_user(user_id: str):

    deleteResult = await users_collection.delete_one({"_id": ObjectId(user_id)})
    if(deleteResult.deleted_count == 0):
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    
    return {"detail": f"{deleteResult.deleted_count} user(s) deleted"}
