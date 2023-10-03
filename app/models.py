# Database models

from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from uuid import UUID, uuid4

from database import Base
from .enums import Role, Status


class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        default=uuid4,
        primary_key=True,
        unique=True,
        index=True,
        nullable=False,
    )
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    role = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)


class Project(Base):
    __tablename__ = "projects"

    id = Column(
        UUID(as_uuid=True),
        default=uuid4,
        primary_key=True,
        unique=True,
        index=True,
        nullable=False,
    )
    title = Column(String, unique=True, index=True)
    description = Column(String)
    assigned_to = Column(Integer, ForeignKey("users.id"))
    status = Column(
        String, default=Status.TODO
    )  # This cannot be Boolean because we have more than 2 statuses
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Task(Base):
    __tablename__ = "tasks"

    id = Column(
        UUID(as_uuid=True),
        default=uuid4,
        primary_key=True,
        unique=True,
        index=True,
        nullable=False,
    )
    name = Column(String, unique=True, index=True)
    description = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    status = Column(
        String, default=Status.TODO
    )  # This cannot be Boolean because we have more than 2 statuses
