# Database models

from sqlalchemy import Boolean, Column, String, DateTime, ForeignKey, Enum, Integer
from sqlalchemy.sql import func
from uuid import uuid4

from database import Base
from .enums import Role, Status


class User(Base):
    __tablename__ = "users"

    id = Column(
        String(36), primary_key=True, default=str(uuid4()), unique=True, index=True
    )
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    role = Column(Enum(Role), index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)


class Project(Base):
    __tablename__ = "projects"

    id = Column(
        String(36), primary_key=True, default=str(uuid4()), unique=True, index=True
    )
    title = Column(String, unique=True, index=True)
    description = Column(String)
    assigned_to = Column(
        String(36), ForeignKey("users.id")
    )  # Because a User's id is a UUID
    status = Column(Enum(Status), default=Status.TODO, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Task(Base):
    __tablename__ = "tasks"

    id = Column(
        String(36), primary_key=True, default=str(uuid4()), unique=True, index=True
    )
    title = Column(String, unique=True, index=True)
    description = Column(String)
    time_spent = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    user_id = Column(
        String(36), ForeignKey("users.id")
    )  # Because a User's id is a UUID
    project_id = Column(
        String(36), ForeignKey("projects.id")
    )  # Because a Project's id is a UUID
    status = Column(Enum(Status), default=Status.TODO, index=True)
