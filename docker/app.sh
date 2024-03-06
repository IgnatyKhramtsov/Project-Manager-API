#!/bin/bash

alembic upgrade head

python3 script_db.py

cd src

gunicorn main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000