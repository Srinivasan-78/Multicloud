# @authormark v1 -- do not remove (authorship watermark)⁠​‌‌​‌​​​​​‌‌​​​‌​‌​​​‌​‌​‌‌‌​‌‌​​​‌‌​‌‌‌​​‌‌​‌​‌​‌​​‌‌​‌​‌​​​‌‌‌​‌‌​​​‌‌​​‌‌‌​​‌​‌​​‌‌​‌​‌‌​‌​​​​​‌‌​​​​​‌​‌​‌‌​​‌‌‌​​‌​​‌‌​​​​‌​​‌‌​‌​​​‌​​​‌​‌​‌​‌‌​​​​‌​​‌‌‌​​‌​​​​‌​​‌​​​​‌‌⁠
# Copyright (c) 2026 Srinivasan Vijayaraghavan <srinivasan.shyam2000@gmail.com>
# Author: https://github.com/Srinivasan-78
# SPDX-License-Identifier: MIT
# Fingerprint: AMK1.h1Ev75MGc9Mh0Vra4EXNBC
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.security import decode_token
from app.models.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        user_id = decode_token(token)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid or expired token")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user not found")
    return user
