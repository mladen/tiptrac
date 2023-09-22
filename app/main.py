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
def read_all_projects():
    return {"Projects": PROJECTS}


@app.get("/projects/{project_id}")
def read_project(project_id: int, q: Union[str, None] = None):
    return {"project_id": project_id, "q": q}
