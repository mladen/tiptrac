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
