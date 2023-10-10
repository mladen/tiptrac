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
    projects: Optional[List[UUID]] = Field(
        default=[], description="List of projects related to this user"
    )  # Optional since not every user might be assigned to a project immediately


class Task(BaseModel):
    id: UUID
    title: str = Field(..., min_length=3, max_length=50)
    description: Optional[str] = Field(
        None, title="Description of the task", max_length=50
    )
    time_estimation: int = Field(
        0, description="Estimated time for the task in minutes"
    )
    time_spent: int = Field(0, description="Time already spent on the task in minutes")
    assigned_to: Optional[UUID] = Field(
        None, description="The user ID responsible for completing this task"
    )
    project_id: UUID  # The project ID to which this task belongs
    status: Status = Field(default=Status.TODO, description="Status of the task")


class Project(BaseModel):
    id: UUID
    title: str = Field(..., min_length=3, max_length=50)
    description: Optional[str] = Field(
        None, title="Description of the project", max_length=50
    )
    time_estimation: int = Field(
        0, description="Estimated time for the project in minutes"
    )
    time_spent: int = Field(
        0, description="Time already spent on the project in minutes"
    )
    assigned_to: Optional[UUID] = Field(
        None, description="The user ID responsible for this project"
    )
    status: Status = Field(default=Status.TODO, description="Status of the project")
    tasks: Optional[List[Task]] = Field(
        default=[], description="List of tasks related to this project"
    )  # Optional since not every project will have tasks immediately
