from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from .enums import Role, Status

from . import models

import bcrypt

password = b"super secret password"
hashed = bcrypt.hashpw(password, bcrypt.gensalt())

if bcrypt.checkpw(password, hashed):
    print("It Matches! The password is: " + password.decode("utf-8"))
else:
    print("It Does not Match :(")


class CreateUser(BaseModel):
    name: str
    email: str
    # role: Role = Role.EMPLOYEE
    password: str


app = FastAPI()


@app.post("/create/user")
async def create_user(user: CreateUser):
    create_user_model = models.User()
    create_user_model.name = user.name
    create_user_model.email = user.email
    # create_user_model.role = user.role
    create_user_model.password = user.password
    create_user_model.hashed_password = user.password
    create_user_model.is_active = True

    return create_user_model
