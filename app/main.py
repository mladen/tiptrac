from typing import Union

from fastapi import FastAPI, APIRouter, HTTPException, Form, Header, Depends, status
from pydantic import UUID4
from typing import Optional, Annotated, List
from uuid import UUID


# from .schemas import User, UserResponse, Project, Task  # importing models
from . import schemas, models  # importing Pydantic models and DB models
from .test_data import PROJECTS, USERS  # importing test data

# from .database import database  # importing database

from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
from .database import engine, SessionLocal  # , Session


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
]  # OpenAPI tags

app = FastAPI(openapi_tags=tags_metadata)

models.Base.metadata.create_all(
    bind=engine
)  # Creates the database tables (if they don't exist) when the application starts


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/", response_model=List[schemas.UserResponse], tags=["users"])
async def read_all(db: Session = Depends(get_db)):
    db_users = db.query(models.User).all()  # Querying the database
    # Converting SQLAlchemy models to Pydantic models before returning
    return [
        schemas.UserResponse(
            id=user.id, name=user.name, email=user.email, role=user.role, projects=[]
        )
        for user in db_users
    ]


# USER
# Login
@app.post("/login/", tags=["users"])
async def login(
    project_position: int,  # Path parameter (required) which represents the position in the PROJECTS list
    username: Optional[str] = Header(None),
    password: Optional[str] = Header(None),
):
    if username == "FastAPIUser" and password == "pwd1234!":
        return PROJECTS[project_position - 1]
    else:
        raise HTTPException(status_code=400, detail="Missing username or password")


# Retrieve all users
@app.get("/users", response_model=List[schemas.UserResponse], tags=["users"])
async def get_users(db: Session = Depends(get_db)):
    db_users = db.query(models.User).all()
    return db_users


# Create a user
@app.post("/users", tags=["users"])
async def create_user(user: schemas.User):
    USERS.append(user)
    return {"User": user}


# Update a user
@app.put("/users/{user_id}", tags=["users"])
async def update_user(user_id: UUID, user: schemas.User):
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
@app.get("/projects", tags=["projects"], response_model=List[schemas.ProjectResponse])
async def get_projects(db: Session = Depends(get_db)):
    db_projects = (
        db.query(models.Project)
        # .options(joinedload(models.Project.users))
        .options(joinedload(models.Project.tasks)).all()  # Eagerly loading tasks
    )
    return db_projects


# Retrieve a project
@app.get(
    "/projects/{project_id}",
    tags=["projects"],  # , response_model=schemas.ProjectResponse
)
async def get_project(project_id: UUID, db: Session = Depends(get_db)):
    print(
        f"Project ID: {project_id}, Type: {type(project_id)}"
    )  # Diagnostic print statement
    db_project = (
        db.query(models.Project)
        # .options(joinedload(models.Project.users))
        .options(joinedload(models.Project.tasks))  # Eagerly loading tasks
        .filter(models.Project.id == str(project_id))  # Ensure project_id is a string
        .first()
    )
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project


# Create a project
@app.post("/projects", response_model=schemas.ProjectResponse, tags=["projects"])
async def create_project(project: schemas.Project, db: Session = Depends(get_db)):
    db_project = models.Project(
        title=project.title,
        description=project.description,
        time_estimation=project.time_estimation,
        time_spent=project.time_spent,
        assigned_to_user=project.assigned_to_user,
        status=project.status,
    )
    try:
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return db_project


# Update a project
@app.put(
    "/projects/{project_id}", response_model=schemas.ProjectResponse, tags=["projects"]
)
async def update_project(
    project_id: UUID, project: schemas.Project, db: Session = Depends(get_db)
):
    # Check if the project exists
    db_project = (
        db.query(models.Project).filter(models.Project.id == str(project_id)).first()
    )
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )

    # Check if the user exists
    if project.assigned_to_user:  # If the user ID is provided
        db_user = (
            db.query(models.User)
            .filter(models.User.id == str(project.assigned_to_user))
            .first()
        )
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

    for key, value in project.dict().items():
        setattr(db_project, key, value) if value else None

    try:
        db.commit()
        db.refresh(db_project)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return db_project


# Delete a project
@app.delete(
    "/projects/{project_id}", response_model=schemas.ProjectResponse, tags=["projects"]
)
async def delete_project(project_id: UUID, db: Session = Depends(get_db)):
    db_project = (
        db.query(models.Project).filter(models.Project.id == str(project_id)).first()
    )
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(db_project)
    db.commit()
    return db_project


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
async def create_project_task(project_id: int, task: schemas.Task):
    PROJECTS[project_id - 1]["tasks"].append(task)
    return {"Task": task}


# Update a task (that belongs to a project)
@app.put("/projects/{project_id}/tasks/{task_id}", tags=["tasks"])
async def update_project_task(project_id: UUID, task_id: UUID, task: schemas.Task):
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
