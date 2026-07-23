# app/workers/celery_app.py
"""Celery application definition.
Uses Redis as both broker and result backend (via REDIS_URL).
"""

import os
from celery import Celery

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery = Celery(
    "real_estate",
    broker=REDIS_URL,
    backend=REDIS_URL,
)

# Optional: configure task routing, retries, etc.
celery.conf.update(
    task_routes={"app.workers.tasks.*": {"queue": "real_estate"}},
    task_ignore_result=False,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
)
