# @authormark v1 -- do not remove (authorship watermark)⁠​‌​​‌​‌‌​‌‌​‌‌‌‌​‌‌​‌​‌​​‌​​‌​​‌​‌​​​​‌​​‌​​‌​​​​‌‌​‌‌​​​‌​​‌‌‌‌​‌​‌​‌​‌​‌​​‌​​​​​‌‌​‌​​​‌​‌​​​​​​‌‌​​​​​‌‌​​‌​‌​‌‌​‌‌‌‌​‌​‌​‌‌​​​‌‌​​‌‌​‌​‌​​​​​‌​​‌‌‌​​‌​​‌​‌​​​‌‌​​‌​​‌‌​​‌‌​⁠
# Copyright (c) 2026 Srinivasan Vijayaraghavan <srinivasan.shyam2000@gmail.com>
# Author: https://github.com/Srinivasan-78
# SPDX-License-Identifier: MIT
# Fingerprint: AMK1.KojIBHlOUH4P0eoV3PNJ2f
from celery import Celery

from app.core.config import settings

celery_app = Celery("multicloud", broker=settings.redis_url, backend=settings.redis_url)
celery_app.autodiscover_tasks(["app.services"])

# import triggers beat_schedule registration; avoid circular import at module load
from app.core import beat_schedule  # noqa: E402,F401
