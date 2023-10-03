# Pydantic models that define and validate the shape of API data

from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID

from .enums import Role, Status


class User(BaseModel):
    id: UUID
    name: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., min_length=3, max_length=50)
    role: Role = Field(..., description="Role of the user")
    projects: List[UUID] = Field(
        [], description="List of projects related to this user"
    )


class Task(BaseModel):
    id: UUID
    title: str = Field(..., min_length=3, max_length=50)
    description: Optional[str] = Field(
        None, title="Description of the task", max_length=50
    )
    time_spent: int = Field(0, description="Time spent on this task in minutes")
    assigned_to: Optional[UUID] = Field(
        None, description="The user ID responsible for completing this task"
    )
    status: Status = Field(..., description="Status of the task", default=Status.TODO)


class Project(BaseModel):
    id: UUID
    title: str = Field(..., min_length=3, max_length=50)
    description: Optional[str] = Field(
        None, title="Description of the project", max_length=50
    )
    assigned_to: Optional[UUID] = Field(
        None, description="The user ID responsible for this project"
    )
    status: Status = Field(
        ..., description="Status of the project", default=Status.TODO
    )
    tasks: List[Task] = Field([], description="List of tasks related to this project")
