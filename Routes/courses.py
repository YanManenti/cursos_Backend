from http import HTTPStatus
from bson import ObjectId
from fastapi import APIRouter, Body, HTTPException
from pymongo import ReturnDocument

from Database.database import courses_collection
from Models.Course import Course, InterestedContact, UpdateCourse, CourseCollection


router = APIRouter(
    prefix="/api/courses",
    tags=["courses"],
)


# Gets all courses from the database and returns them as a list
@router.get("/",
            response_model = CourseCollection,
            response_model_by_alias = False
            )
async def read_all_courses():

    data = []
    cursor = courses_collection.find()

    for document in await cursor.to_list(length=100):
        data.append(document)

    return CourseCollection(courses=data)


# Gets a course by their Id
@router.get("/{course_id}",
            response_model = Course,
            response_model_by_alias = False
            )
async def read_course(course_id: str):

    course = await courses_collection.find_one({"_id": ObjectId(course_id)})
    if(course is None):
        return HTTPException(status_code=404, detail="Course not found")
    
    return course


# Creates a new course
@router.post("/",
             response_model = Course,
             status_code=HTTPStatus.CREATED,
             response_model_by_alias = False
             )
async def create_course(course: Course = Body(...)):
    
    newCourse = await courses_collection.insert_one(course.model_dump(by_alias=True, exclude=["id"]))
    if(newCourse is None):
        return HTTPException(status_code=404, detail="Error creating course")
    
    createdCourse = await courses_collection.find_one({"_id": newCourse.inserted_id})
    if(createdCourse is None):
        return HTTPException(status_code=404, detail="Error finding created course")
    
    return createdCourse


# Updates a course by their Id
@router.put("/{course_id}",
            response_model = Course,
            response_model_by_alias = False
            )
async def update_course(course_id: str, course: UpdateCourse = Body(...)):
    
    # Iterates through the received course dictionary and removes any None values
    course={
        key: value for key, value in course.model_dump(by_alias=True).items() if value is not None
    }

    updatedCourse = await courses_collection.find_one_and_update({"_id": ObjectId(course_id)}, {"$set": course}, return_document=ReturnDocument.AFTER)
    if(updatedCourse is None):
        return HTTPException(status_code=404, detail="Error updating course")
    
    updatedCourse = await courses_collection.find_one({"_id": ObjectId(course_id)})
    if(updatedCourse is None):
        return HTTPException(status_code=404, detail="Error finding updated course")
    
    return updatedCourse


# Patches a course by Id to have a new InterestedContact
@router.patch("/{course_id}/add-interested",
              response_model = Course,
              response_model_by_alias = False
              )
async def patch_course(course_id: str, interested_contact: InterestedContact = Body(...)):

    # Iterates through the received interested_contact dictionary and removes any None values
    interested_contact={
        key: value for key, value in interested_contact.model_dump(by_alias=True).items() if value is not None
    }
    
    courseInDb = await courses_collection.find_one({"_id": ObjectId(course_id)})
    if(courseInDb is None):
        return HTTPException(status_code=404, detail="Course not found")
    
    currentInterestedList = courseInDb.get("interested_list") or []
    if(currentInterestedList.count(interested_contact) > 0):
        return HTTPException(status_code=400, detail="Contact already in interested list")

    currentInterestedList.append(interested_contact)
    updatedCourse = await courses_collection.find_one_and_update({"_id": ObjectId(course_id)}, {"$set": {"interested_list": currentInterestedList}}, return_document=ReturnDocument.AFTER)
    if(updatedCourse is None):
        return HTTPException(status_code=404, detail="Error updating course")
            
    return updatedCourse


# Patches a course by Id to remove a InterestedContact
@router.patch("/{course_id}/remove-interested",
              response_model = Course,
              response_model_by_alias = False
              )
async def patch_course(course_id: str, interested_contact: InterestedContact = Body(...)):

    # Iterates through the received interested_contact dictionary and removes any None values
    interested_contact={
        key: value for key, value in interested_contact.model_dump(by_alias=True).items() if value is not None
    }
    
    courseInDb = await courses_collection.find_one({"_id": ObjectId(course_id)})
    if(courseInDb is None):
        return HTTPException(status_code=404, detail="Course not found")
    
    currentInterestedList = courseInDb.get("interested_list") or []

    if(currentInterestedList.index(interested_contact) == -1):
        return HTTPException(status_code=404, detail="Contact not found in interest list")

    currentInterestedList.remove(interested_contact)
    updatedCourse = await courses_collection.find_one_and_update({"_id": ObjectId(course_id)}, {"$set": {"interested_list": currentInterestedList}}, return_document=ReturnDocument.AFTER)
    if(updatedCourse is None):
        return HTTPException(status_code=404, detail="Error updating course")
            
    return updatedCourse


# Deletes a course by their Id
@router.delete("/{course_id}")
async def delete_course(course_id: str):

    deleteResult = await courses_collection.delete_one({"_id": ObjectId(course_id)})
    if(deleteResult.deleted_count == 0):
        return HTTPException(status_code=404, detail="Course not found")
    
    return {"detail": f"{deleteResult.deleted_count} course(s) deleted"}

