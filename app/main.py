import os
from fastapi import FastAPI

from app.Routes import courses, users
# from Routes import courses, users
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:3000/",
    "http://localhost:8000",
    "http://localhost:8000/",
    "172.18.0.4:3000",
    "172.18.0.4:3000/",
    "0.0.0.0:3000",
    "0.0.0.0:3000/",
    "127.0.0.1:3000",
    "127.0.0.1:3000/",
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