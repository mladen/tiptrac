# Pydantic models that define and validate the shape of API data

from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID, uuid4

from .enums import Role, Status

# TaskRef = ForwardRef("Task")
# ProjectRef = ForwardRef("Project")


class Task(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str = Field(..., min_length=3, max_length=50)
    description: Optional[str] = Field(
        None, title="Description of the task", max_length=255
    )
    time_estimation: Optional[int] = Field(
        0, description="Estimated time for the task in minutes"
    )
    time_spent: Optional[int] = Field(
        0, description="Time already spent on the task in minutes"
    )
    assigned_to_user: Optional[UUID] = Field(
        None, description="The user ID responsible for completing this task"
    )
    belongs_to_project: Optional[UUID] = Field(
        None, description="The project ID this task is related to"
    )  # The project ID to which this task belongs
    status: Status = Field(default=Status.TODO, description="Status of the task")


class TaskResponse(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str = Field(..., min_length=3, max_length=50)
    description: Optional[str] = Field(
        None, title="Description of the task", max_length=255
    )
    time_estimation: Optional[int] = Field(
        0, description="Estimated time for the task in minutes"
    )
    time_spent: Optional[int] = Field(
        0, description="Time already spent on the task in minutes"
    )
    assigned_to_user: Optional[UUID] = Field(
        None, description="The user ID responsible for completing this task"
    )
    belongs_to_project: Optional[UUID] = Field(
        None, description="The project ID this task is related to"
    )  # The project ID to which this task belongs
    status: Status = Field(default=Status.TODO, description="Status of the task")

    class Config:
        from_attributes = True


class Project(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str = Field(..., min_length=3, max_length=50)
    description: Optional[str] = Field(
        None, title="Description of the project", max_length=255
    )
    time_estimation: Optional[int] = Field(
        0, description="Estimated time for the project in minutes"
    )
    time_spent: Optional[int] = Field(
        0, description="Time already spent on the project in minutes"
    )
    assigned_to_user: Optional[UUID] = Field(
        None, description="The user ID responsible for this project"
    )
    status: Status = Field(default=Status.TODO, description="Status of the project")
    tasks: Optional[List[Task]] = Field(
        default=[], description="List of tasks related to this project"
    )  # Optional since not every project will have tasks immediately


class ProjectResponse(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str = Field(..., min_length=3, max_length=50)
    description: Optional[str] = Field(
        None, title="Description of the project", max_length=255
    )
    time_estimation: Optional[int] = Field(
        0, description="Estimated time for the project in minutes"
    )
    time_spent: Optional[int] = Field(
        0, description="Time already spent on the project in minutes"
    )
    assigned_to_user: Optional[UUID] = Field(
        None, description="The user ID responsible for this project"
    )
    status: Status = Field(default=Status.TODO, description="Status of the project")
    tasks: Optional[List[Task]] = Field(
        default=[], description="List of tasks related to this project"
    )  # Optional since not every project will have tasks immediately

    class Config:
        from_attributes = True


class User(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., min_length=3, max_length=50)
    role: Role = Field(..., description="Role of the user")
    hashed_password: str = Field(..., min_length=10, max_length=255)
    projects: Optional[List[Project]] = Field(
        default=[], description="List of projects related to this user"
    )  # Optional since not every user might be assigned to a project immediately


class UserResponse(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., min_length=3, max_length=50)
    role: Role = Field(..., description="Role of the user")
    projects: Optional[List[Project]] = Field(
        default=[], description="List of projects related to this user"
    )  # Optional since not every user might be assigned to a project immediately

    class Config:
        from_attributes = True
