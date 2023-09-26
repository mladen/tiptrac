from typing import Union

from fastapi import FastAPI, APIRouter, HTTPException
from .models import Project, Task  # importing models
from .test_data import PROJECTS  # importing test data

tags_metadata = [
    {
        "name": "projects",
        "description": "Operations related to projects.",
    },
    {
        "name": "tasks",
        "description": "Operations related to tasks within projects.",
    },
]

app = FastAPI(openapi_tags=tags_metadata)


# GET
# Retrieve all projects
@app.get("/", tags=["projects"])
async def get_all_projects():
    return {"Projects": PROJECTS}


# Retrieve a project
@app.get("/projects/{project_id}", tags=["projects"])
async def get_project(project_id: int):
    return PROJECTS[project_id - 1]


# Retrieve all tasks from a project
@app.get("/projects/{project_id}/tasks", tags=["tasks"])
async def get_project_tasks(project_id: int):
    return PROJECTS[project_id - 1]["tasks"]


# Retrieve a task from a project
@app.get("/projects/{project_id}/tasks/{task_id}", tags=["tasks"])
async def get_project_task(project_id: int, task_id: int):
    return PROJECTS[project_id - 1]["tasks"][task_id - 1]


# POST
# Post a project
@app.post("/projects", tags=["projects"])
async def create_project(project: Project):
    PROJECTS.append(project)
    return {"Project": project}


# Post a task to a project
@app.post("/projects/{project_id}/tasks", tags=["tasks"])
async def create_project_task(project_id: int, task: dict):
    PROJECTS[project_id - 1]["tasks"].append(task)
    return {"Task": task}
