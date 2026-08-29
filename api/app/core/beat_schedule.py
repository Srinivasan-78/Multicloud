# @authormark v1 -- do not remove (authorship watermark)⁠​‌​‌​‌‌​​‌​​​​‌​​‌‌‌​​‌​​‌‌​‌‌‌​​‌​​‌‌‌‌​‌​​​‌‌​​‌‌​​​‌​​‌​​​​‌‌​‌‌​‌‌‌‌​‌‌​​‌​​​​‌‌​‌‌​​​‌‌‌​​​​‌​‌​​‌‌​‌‌‌​‌​​​‌​‌​​‌​​‌‌​‌​‌​​‌‌‌​‌​​​‌‌‌​​​‌​‌‌​​‌​‌​‌​​‌‌‌​​‌‌​​‌‌​​‌​‌​​​​⁠
# Copyright (c) 2026 Srinivasan Vijayaraghavan <srinivasan.shyam2000@gmail.com>
# Author: https://github.com/Srinivasan-78
# SPDX-License-Identifier: MIT
# Fingerprint: AMK1.VBrnOFbCod68StRjtqeNfP
from celery.schedules import crontab

from app.core.celery_app import celery_app

celery_app.conf.beat_schedule = {
    "sweep-expired-resources-hourly": {
        "task": "sweep_expired_resources",
        "schedule": crontab(minute=0),  # top of every hour
    },
}
