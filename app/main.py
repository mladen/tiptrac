from typing import Union

from fastapi import FastAPI

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


@app.get("/")
def get_all_projects():
    return {"Projects": PROJECTS}


@app.get("/projects/{project_id}")
def get_project(project_id: int):
    return PROJECTS[project_id - 1]


# Retrieve all tasks from a project
@app.get("/projects/{project_id}/tasks")
def get_project_tasks(project_id: int):
    return PROJECTS[project_id - 1]["tasks"]


# Retrieve a task from a project
@app.get("/projects/{project_id}/tasks/{task_id}")
def get_project_task(project_id: int, task_id: int):
    return PROJECTS[project_id - 1]["tasks"][task_id - 1]
