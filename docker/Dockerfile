# Pull official base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y gcc python3-dev musl-dev libmagic1 libffi-dev netcat

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

# Copy entrypoint.sh
COPY ./docker/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

# COPY ./alembic.ini /alembic.ini
# COPY ./migrations /migrations

COPY ./app /app

# ENTRYPOINT [ "/entrypoint.sh" ]
