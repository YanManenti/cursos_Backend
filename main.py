from typing import Annotated
from fastapi import FastAPI
from pydantic import BeforeValidator

from Routes import courses, users

app = FastAPI()

app.include_router(users.router)
app.include_router(courses.router)

