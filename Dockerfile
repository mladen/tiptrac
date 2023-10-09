# Use the official Python image from the DockerHub
FROM python:3.11

# Set the working directory in the container
WORKDIR /code

# Copy the dependencies file to the working directory
COPY ./requirements.txt /code/requirements.txt

# Install any dependencies
RUN pip install --no-cache-dir -r /code/requirements.txt

# Copy the content of the local src directory to the working directory
COPY ./app /code/app

# Specify the command to run on container start
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
