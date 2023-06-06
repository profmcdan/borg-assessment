#!/bin/sh

#alembic revision --autogenerate -m "Deploy"
alembic upgrade head

exec "$@"
