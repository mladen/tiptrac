from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from .enums import Role, Status

from . import models
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from .database import SessionLocal, engine

import bcrypt


class CreateUser(BaseModel):
    name: str
    email: str
    # role: Role = Role.EMPLOYEE
    password: str


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/create/user")
async def create_user(user: CreateUser, db: Session = Depends(get_db)):
    existing_user = (
        db.query(models.User).filter(models.User.email == user.email).first()
    )
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    create_user_model = models.User()
    create_user_model.name = user.name
    create_user_model.email = user.email
    # create_user_model.role = user.role

    create_user_model.hashed_password = bcrypt.hashpw(
        user.password.encode(
            "utf-8"
        ),  # user.password.encode("utf-8") encodes the password to bytes
        bcrypt.gensalt(),
    )

    create_user_model.is_active = True

    try:
        db.add(create_user_model)
        db.commit()
        db.refresh(create_user_model)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
