from celery.schedules import crontab

from app.core.celery_app import celery_app

celery_app.conf.beat_schedule = {
    "sweep-expired-resources-hourly": {
        "task": "sweep_expired_resources",
        "schedule": crontab(minute=0),  # top of every hour
    },
}
