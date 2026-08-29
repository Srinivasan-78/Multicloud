# @authormark v1 -- do not remove (authorship watermark)⁠​‌​‌​‌​‌​‌​‌‌​​‌​‌‌‌​​​‌​‌‌‌​​‌‌​‌​​‌​​​​‌‌​‌​​‌​‌​‌​‌​‌​‌‌‌​‌‌​​‌​‌​‌‌‌​‌‌​‌‌‌​​​‌‌‌​​‌​​‌‌​​​​​‌‌‌​​‌‌​‌​​​​​‌​‌​‌‌​​‌​‌​​​​‌​​‌‌‌​​​‌​‌‌​​‌‌‌​‌​​‌‌​​​‌‌‌‌​​​​‌​‌​​​‌​‌‌‌​‌​‌⁠
# Copyright (c) 2026 Srinivasan Vijayaraghavan <srinivasan.shyam2000@gmail.com>
# Author: https://github.com/Srinivasan-78
# SPDX-License-Identifier: MIT
# Fingerprint: AMK1.UYqsHiUvWn90sAYBqgLxQu
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
