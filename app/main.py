from typing import Union

from fastapi import FastAPI

app = FastAPI()

TASKS = [
    {
        "id": 1,
        "title": "Buy groceries",
        "description": "Milk, Cheese, Pizza, Fruit",
        "done": False,
    },
    {
        "id": 2,
        "title": "Create a Time and Project Tracker",
        "description": "Need to create a time and project tracker for myself",
        "done": False,
    },
]


@app.get("/")
def read_all_tasks():
    return {"Tasks": TASKS}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
