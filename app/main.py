from fastapi import FastAPI

from app.Routes import courses, users


app = FastAPI()

app.include_router(users.router)
app.include_router(courses.router)