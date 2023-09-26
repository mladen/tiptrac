from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID, uuid4

app = FastAPI()

PROJECTS = [
    {
        "id": uuid4(),
        "title": "Create a Time and Project Tracker",
        "description": "Need to create a time and project tracker for myself",
        "assigned_to": None,
        "done": False,
        "tasks": [
            {
                "id": uuid4(),
                "title": "Setup the project",
                "description": "Setup the project with FastAPI",
                "time_spent": 0,  # Time spent on this task
                "assigned_to": None,  # The person responsible for completing this task
                "done": False,
            },
            {
                "id": uuid4(),
                "title": "Create the project model",
                "description": "Create the project model with Pydantic",
                "time_spent": 0,
                "assigned_to": None,
                "done": False,
            },
            {
                "id": uuid4(),
                "title": "Create the project endpoints",
                "description": "Create the project endpoints with FastAPI",
                "time_spent": 0,
                "assigned_to": None,
                "done": False,
            },
            {
                "id": uuid4(),
                "title": "Create the project database",
                "description": "Create the project database with SQLAlchemy",
                "time_spent": 0,
                "assigned_to": None,
                "done": False,
            },
        ],
    }
]


class Task(BaseModel):
    id: UUID
    title: str = Field(..., min_length=3, max_length=50)
    description: Optional[str] = Field(
        None, title="Description of the task", min_length=3, max_length=50
    )
    time_spent: int = Field(0, description="Time spent on this task in minutes")
    assigned_to: Optional[str] = Field(
        None,
        description="The person responsible for completing this task",
        min_length=3,
        max_length=50,
    )
    done: bool = False


class Project(BaseModel):
    id: UUID
    title: str = Field(..., min_length=3, max_length=50)
    description: Optional[str] = Field(
        None, title="Description of the project", min_length=3, max_length=50
    )
    assigned_to: Optional[str] = Field(
        None,
        description="The person responsible for this project",
        min_length=3,
        max_length=50,
    )
    done: bool = False
    tasks: List[Task] = Field([], description="List of tasks related to this project")


# GET
# Retrieve all projects
@app.get("/")
async def get_all_projects():
    return {"Projects": PROJECTS}


# Retrieve a project
@app.get("/projects/{project_id}")
async def get_project(project_id: int):
    return PROJECTS[project_id - 1]


# Retrieve all tasks from a project
@app.get("/projects/{project_id}/tasks")
async def get_project_tasks(project_id: int):
    return PROJECTS[project_id - 1]["tasks"]


# Retrieve a task from a project
@app.get("/projects/{project_id}/tasks/{task_id}")
async def get_project_task(project_id: int, task_id: int):
    return PROJECTS[project_id - 1]["tasks"][task_id - 1]


# POST
# Post a project
@app.post("/projects")
async def create_project(project: Project):
    PROJECTS.append(project)
    return {"Project": project}


# Post a task to a project
@app.post("/projects/{project_id}/tasks")
async def create_project_task(project_id: int, task: dict):
    PROJECTS[project_id - 1]["tasks"].append(task)
    return {"Task": task}
