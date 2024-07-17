import os
from fastapi import FastAPI

from app.Routes import courses, users
# from Routes import courses, users
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:3000/",
    "http://localhost:8080",
    os.getenv('FRONTEND_URL')
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(users.router)
app.include_router(courses.router)