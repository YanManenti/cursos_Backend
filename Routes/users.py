from fastapi import APIRouter
from Database.database import users_collection


router = APIRouter(
    prefix="/api/users",
    tags=["users"],
)

@router.get("/")
async def read_all_users():
    data = []
    cursor = users_collection.find()
    for document in await cursor.to_list(length=100):
        data.append(document)
    return repr(data)

@router.get("/{user_id}")
async def read_user(user_id: str):
    user = await users_collection.find_one({"_id": user_id})
    return repr(user)

@router.post("/")
async def create_user(user: dict):
    user = await users_collection.insert_one(user)
    return repr(user)

@router.put("/{user_id}")
async def update_user(user_id: str, user: dict):
    user = await users_collection.update_one({"_id": user_id}, {"$set": user})
    return repr(user)

@router.delete("/{user_id}")
async def delete_user(user_id: str):
    user = await users_collection.delete_one({"_id": user_id})
    return repr(user)
