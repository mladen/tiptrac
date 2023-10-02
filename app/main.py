from typing import Union

from fastapi import FastAPI, APIRouter, HTTPException, Form, Header
from pydantic import UUID4
from uuid import UUID

from .models import User, Project, Task  # importing models
from .test_data import PROJECTS, USERS  # importing test data


tags_metadata = [
    {
        "name": "users",
        "description": "Operations related to users.",
    },
    {
        "name": "projects",
        "description": "Operations related to projects.",
    },
    {
        "name": "tasks",
        "description": "Operations related to tasks within projects.",
    },
    {
        "name": "header",
        "description": "Operations related to headers.",
    },
]

app = FastAPI(openapi_tags=tags_metadata)


# Header
@app.post("/header", tags=["header"])
async def get_header(random_header: str = Header(None)):
    return {"Random-Header": random_header}


# USER
# Login
@app.post("/login", tags=["users"])
async def login(username: str = Form(), password: str = Form()):
    return {"username": username, "password": password}


# Retrieve all users
@app.get("/users", tags=["users"])
async def get_all_users():
    return {"Users": USERS}


# Create a user
@app.post("/users", tags=["users"])
async def create_user(user: User):
    USERS.append(user)
    return {"User": user}


# Update a user
@app.put("/users/{user_id}", tags=["users"])
async def update_user(user_id: UUID, user: User):
    # Check if the user exists
    existing_user = next((usr for usr in USERS if usr["id"] == user_id), None)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Logic for updating the user
    index = USERS.index(existing_user)
    USERS[index] = user.dict()
    USERS[index]["id"] = user_id


# Delete a user
@app.delete("/users/{user_id}", tags=["users"])
async def delete_user(user_id: UUID):
    # Check if the user exists
    existing_user = next((usr for usr in USERS if usr["id"] == user_id), None)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Logic for deleting the user
    USERS.remove(existing_user)
    return {"message": "User deleted successfully"}


# Retrieve a user
# @app.get("/users/{user_id}", tags=["users"])
# async def get_user(user_id: UUID4):
#     return {"User": {}}


# Retrieve all projects for a user
# @app.get("/users/{user_id}/projects", tags=["projects"])
# async def get_user_projects(user_id: UUID4):
#     return {"Projects": []}


# Retrieve a project for a user
# @app.get("/users/{user_id}/projects/{project_id}", tags=["projects"])
# async def get_user_project(user_id: UUID4, project_id: UUID4):
#     return {"Project": {}}


# Retrieve all tasks for a user
# @app.get("/users/{user_id}/tasks", tags=["tasks"])
# async def get_user_tasks(user_id: UUID4):
#     return {"Tasks": []}


# Retrieve a task for a user
# @app.get("/users/{user_id}/tasks/{task_id}", tags=["tasks"])
# async def get_user_task(user_id: UUID4, task_id: UUID4):
#     return {"Task": {}}


# PROJECT
# Retrieve all projects
@app.get("/projects", tags=["projects"])
async def get_all_projects():
    return {"Projects": PROJECTS}


# Retrieve a project
@app.get("/projects/{project_id}", tags=["projects"])
async def get_project(project_id: int):
    return PROJECTS[project_id - 1]


# Create a project
@app.post("/projects", tags=["projects"])
async def create_project(project: Project):
    PROJECTS.append(project)
    return {"Project": project}


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


# Delete a project
@app.delete("/projects/{project_id}", tags=["projects"])
async def delete_project(project_id: UUID):
    # Check if the project exists
    existing_project = next(
        (proj for proj in PROJECTS if proj["id"] == project_id), None
    )
    if not existing_project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Logic for deleting the project
    PROJECTS.remove(existing_project)
    return {"message": "Project deleted successfully"}


# TASK
# Retrieve all tasks from a project
@app.get("/projects/{project_id}/tasks", tags=["tasks"])
async def get_project_tasks(project_id: int):
    return PROJECTS[project_id - 1]["tasks"]


# Retrieve a task from a project
# @app.get("/projects/{project_id}/tasks/{task_id}", tags=["tasks"])
# async def get_project_task(project_id: int, task_id: int):
#     return PROJECTS[project_id - 1]["tasks"][task_id - 1]


# Create a task for a project
@app.post("/projects/{project_id}/tasks", tags=["tasks"])
async def create_project_task(project_id: int, task: Task):
    PROJECTS[project_id - 1]["tasks"].append(task)
    return {"Task": task}


# Update a task (that belongs to a project)
@app.put("/projects/{project_id}/tasks/{task_id}", tags=["tasks"])
async def update_project_task(project_id: UUID, task_id: UUID, task: Task):
    # Check if the project exists
    existing_project = next(
        (proj for proj in PROJECTS if proj["id"] == project_id), None
    )
    if not existing_project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Check if the task exists
    existing_task = next(
        (tsk for tsk in existing_project["tasks"] if tsk["id"] == task_id), None
    )
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Logic for updating the task
    index = existing_project["tasks"].index(existing_task)
    existing_project["tasks"][index] = task.dict()
    existing_project["tasks"][index]["id"] = task_id

    return {"Task": task}


# Delete a task
@app.delete("/projects/{project_id}/tasks/{task_id}", tags=["tasks"])
async def delete_project_task(project_id: UUID, task_id: UUID):
    # Check if the project exists
    existing_project = next(
        (proj for proj in PROJECTS if proj["id"] == project_id), None
    )
    if not existing_project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Check if the task exists
    existing_task = next(
        (tsk for tsk in existing_project["tasks"] if tsk["id"] == task_id), None
    )
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Logic for deleting the task
    existing_project["tasks"].remove(existing_task)
    return {"message": "Task deleted successfully"}
