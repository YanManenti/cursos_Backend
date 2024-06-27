from fastapi import APIRouter, Body

from Database.database import courses_collection
from Models.Course import Course, UpdateCourse, CourseCollection


router = APIRouter(
    prefix="/api/courses",
    tags=["courses"],
)

@router.get("/",
            response_model = CourseCollection,
            response_model_by_alias = False
            )
async def read_all_courses():
    data = []
    cursor = courses_collection.find()
    for document in await cursor.to_list(length=100):
        data.append(document)
    return repr(data)

@router.get("/{course_id}",
            response_model = Course,
            response_model_by_alias = False
            )
async def read_course(course_id: str):
    course = await courses_collection.find_one({"_id": course_id})
    return repr(course)

@router.post("/",
             response_model = Course,
             response_model_by_alias = False
             )
async def create_course(course: Course = Body(...)):
    course = await courses_collection.insert_one(course)
    return repr(course)

@router.put("/{course_id}",
            response_model = Course,
            response_model_by_alias = False
            )
async def update_course(course_id: str, course: UpdateCourse = Body(...)):
    course = await courses_collection.update_one({"_id": course_id}, {"$set": course})
    return repr(course)

@router.delete("/{course_id}",
               response_model = Course,
               response_model_by_alias = False
               )
async def delete_course(course_id: str):
    course = await courses_collection.delete_one({"_id": course_id})
    return repr(course)

