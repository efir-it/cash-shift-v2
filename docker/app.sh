#!/bin/bash

alembic upgrade head
gunicorn main:app --proxy-protocol  --proxy-allow-from '*' --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:6013

