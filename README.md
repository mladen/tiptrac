# Building a REST API using FastAPI and Docker

## Requirements

- Docker
- Docker Compose
- Python 3.10+

## Installation

> Do only the first time

```bash
$ docker-compose build
```

> Running the Docker containers

```bash
$ docker-compose up
```

# Test server

to check the project our Docker container's URL, visit http://127.0.0.1/items/5?q=somequery
We will see something like:

```json
{ "item_id": 5, "q": "somequery" }
```

# Documentation

## Automatic interactive API documentation (Swagger UI)

To see the automatic interactive API documentation (provided by Swagger UI) visit http://127.0.0.1/docs

## Alternative automatic documentation (ReDoc)

Go to http://127.0.0.1/redoc

You will see the alternative automatic documentation (provided by ReDoc)

## Explanation about the circular references in schemes.py

### What's exactly circular in my code?

In my code, the Project model references the Task model in its tasks field, and the Task model references the User model in its user field. Additionally, the User model references the Project model in its projects field. This creates a circular dependency, as each model references another, and at some point, one of the models references back to a starting point in this dependency chain. The use of ForwardRef and update_forward_refs() helps to resolve these circular dependencies by deferring the resolution of the model references until all models have been defined.

### Why don't I need to update the User model being referenced in the Task model?

In my code, the User model is defined before the Task model. Therefore, when the Task model references the User model, the User model has already been fully defined, and there's no need to use ForwardRef or update_forward_refs(). However, the Project model references the Task model, and Task references Project creating a circular dependency between them, which is why ForwardRef and update_forward_refs() are necessary in this case.

# Is there a better way to do it (without using ForwardRef and update_forward_refs())?

One way to simplify my schemas and avoid circular dependencies is by separating the schemas into different files or utilizing fewer nested models. I might consider creating a separate file for each model or creating a separate file for shared or common models. This way, I can import models without running into circular dependencies, which should simplify the structure of my schemas and make the relationships between different models clearer.
