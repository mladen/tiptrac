from typing import Union

from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import UUID4
from uuid import UUID

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
async def create_project_task(project_id: int, task: Task):
    PROJECTS[project_id - 1]["tasks"].append(task)
    return {"Task": task}


# PUT
# Update a project
@app.put("/projects/{project_id}", tags=["projects"])
async def update_project(project_id: UUID, project: Project):
    # Check if the project exists
    existing_project = next(  # next() returns the next item in an iterator
        (proj for proj in PROJECTS if proj["id"] == project_id), None
    )
    if not existing_project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Logic for updating the project
    index = PROJECTS.index(existing_project)
    PROJECTS[index] = project.dict()
    PROJECTS[index]["id"] = project_id  # Ensure we maintain the original UUID

    return {"Project": project}
