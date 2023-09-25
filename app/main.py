from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

PROJECTS = [
    {
        "id": 1,
        "title": "Create a Time and Project Tracker",
        "description": "Need to create a time and project tracker for myself",
        "done": False,
        "tasks": [
            {
                "id": 1,
                "title": "Setup the project",
                "description": "Setup the project with FastAPI",
                "done": False,
            },
            {
                "id": 2,
                "title": "Create the project model",
                "description": "Create the project model with Pydantic",
                "done": False,
            },
            {
                "id": 3,
                "title": "Create the project endpoints",
                "description": "Create the project endpoints with FastAPI",
                "done": False,
            },
            {
                "id": 4,
                "title": "Create the project database",
                "description": "Create the project database with SQLAlchemy",
                "done": False,
            },
            {
                "id": 5,
                "title": "Create the project database",
                "description": "Create the project database with SQLAlchemy",
                "done": False,
            },
        ],
    }
]


class Task(BaseModel):
    id: int
    title: str
    description: str
    done: bool


class Project(BaseModel):
    id: int
    title: str
    description: str
    done: bool
    tasks: List[Task]


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
