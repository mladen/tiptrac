# Database models

from sqlalchemy import Boolean, Column, String, DateTime, ForeignKey, Enum, Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from uuid import uuid4

from .database import Base
from .enums import Role, Status


class User(Base):
    __tablename__ = "users"

    id = Column(
        String(36), primary_key=True, default=str(uuid4()), unique=True, index=True
    )
    name = Column(String(50), unique=True, index=True)
    email = Column(String(70), unique=True, index=True)
    role = Column(Enum(Role), index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    projects = relationship("Project", back_populates="user")
    tasks = relationship("Task", back_populates="user")


class Project(Base):
    __tablename__ = "projects"

    id = Column(
        String(36), primary_key=True, default=str(uuid4()), unique=True, index=True
    )
    title = Column(String(255), unique=True, index=True)
    description = Column(String(255))

    assigned_to_user = Column(
        String(36), ForeignKey("users.id")
    )  # Because a User's id is a UUID

    status = Column(Enum(Status), default=Status.TODO, index=True)

    time_estimation = Column(
        Integer, default=0
    )  # Estimated time for the project in minutes
    time_spent = Column(
        Integer, default=0
    )  # Time already spent on the project in minutes

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="projects")
    tasks = relationship("Task", back_populates="project")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(
        String(36), primary_key=True, default=str(uuid4()), unique=True, index=True
    )
    title = Column(String(255), unique=True, index=True)
    description = Column(String(255))

    assigned_to_user = Column(
        String(36), ForeignKey("users.id")
    )  # Because a User's id is a UUID
    belongs_to_project = Column(
        String(36), ForeignKey("projects.id")
    )  # Because a Project's id is a UUID
    status = Column(Enum(Status), default=Status.TODO, index=True)

    time_estimation = Column(
        Integer, default=0
    )  # Estimated time for the task in minutes
    time_spent = Column(Integer, default=0)  # Time already spent on the task in minutes

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="tasks")
    project = relationship("Project", back_populates="tasks")
