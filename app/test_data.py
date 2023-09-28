from uuid import uuid4

USERS = [
    {
        "id": uuid4(),
        "name": "John Doe",
        "email": "johndoe@email.com",
        "role": "admin",
        "projects": [],
    },
    {
        "id": uuid4(),
        "name": "Jane Doe",
        "email": "janedoe@email.com",
        "role": "manager",
        "projects": [],
    },
    {
        "id": uuid4(),
        "name": "John Smith",
        "email": "johnsmith@email.com",
        "role": "user",
        "projects": [],
    },
]

PROJECTS = [
    {
        "id": uuid4(),
        "title": "Create a Time and Project Tracker",
        "description": "Need to create a time and project tracker for myself",
        "assigned_to": None,
        "done": False,
        "status": "todo",
        "tasks": [
            {
                "id": uuid4(),
                "title": "Setup the project",
                "description": "Setup the project with FastAPI",
                "time_spent": 0,  # Time spent on this task
                "assigned_to": None,  # The person responsible for completing this task
                "done": True,
                "status": "done",
            },
            {
                "id": uuid4(),
                "title": "Create the project model",
                "description": "Create the project model with Pydantic",
                "time_spent": 0,
                "assigned_to": None,
                "done": False,
                "status": "in_progress",
            },
            {
                "id": uuid4(),
                "title": "Create the project endpoints",
                "description": "Create the project endpoints with FastAPI",
                "time_spent": 0,
                "assigned_to": None,
                "done": False,
                "status": "in_progress",
            },
            {
                "id": uuid4(),
                "title": "Create the project database",
                "description": "Create the project database with SQLAlchemy",
                "time_spent": 0,
                "assigned_to": None,
                "done": False,
                "status": "todo",
            },
        ],
    }
]
