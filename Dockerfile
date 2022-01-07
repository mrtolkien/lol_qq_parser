FROM tiangolo/uvicorn-gunicorn-fastapi:latest

# Run `docker build --no-cache .` when you get a pip warning
RUN /usr/local/bin/python -m pip install --upgrade pip

#################
# POETRY INSTALL
#################

# Installing poetry with pip, ok in this use-case imo
RUN pip install poetry==1.1.12

# Telling poetry to run in the global environment
RUN poetry config virtualenvs.create false

# Copying the project files, install will use versions from poetry.lock
COPY poetry.lock .
COPY pyproject.toml .

# Installing only production dependencies
#   FastAPI is installed already in the Docker image
RUN poetry install --no-dev --no-root -vv

# This is not in the image but FastAPI requires it...
RUN pip install click

# We copy all the lol_data_api folder inside /app as it is where the Docker images looks for the API
COPY ./app /app/app

# The run command is already handled by the parent image
