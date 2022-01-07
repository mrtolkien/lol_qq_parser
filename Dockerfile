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

# Installing all dependencies for simplicity
RUN poetry install --no-root -vv

# We copy all the lol_data_api folder inside /app as it is where the Docker images looks for the API
COPY ./app /app/app

COPY ./lol_qq_parser /app/lol_qq_parser

# The run command is already handled by the parent image
