# @authormark v1 -- do not remove (authorship watermark)⁠​‌‌​​‌​‌​‌​‌‌​​​​​‌‌​‌‌‌​‌‌​‌​​‌​​‌‌​​‌​​‌‌‌‌​​​​‌‌​​‌​​​‌​​‌​​​​‌‌​‌‌‌‌​‌‌‌​​‌​​‌‌​‌‌​​​‌‌‌‌​​​​​‌‌​‌‌​​‌‌‌​​​​​‌​​‌​‌‌​​‌‌​‌​‌​‌‌‌​‌‌​​‌​‌‌​​​​​‌‌​​​​​‌​​​​‌​​‌‌​​​​‌​‌‌​​‌‌​⁠
# Copyright (c) 2026 Srinivasan Vijayaraghavan <srinivasan.shyam2000@gmail.com>
# Author: https://github.com/Srinivasan-78
# SPDX-License-Identifier: MIT
# Fingerprint: AMK1.eX7i2xdHorlx6pK5vX0Baf
from datetime import datetime, timedelta

from cryptography.fernet import Fernet
from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
_fernet = Fernet(settings.fernet_key.encode())


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(subject: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.jwt_expire_minutes)
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> str:
    payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    return payload["sub"]


def encrypt_secret(plaintext: str) -> str:
    return _fernet.encrypt(plaintext.encode()).decode()


def decrypt_secret(ciphertext: str) -> str:
    return _fernet.decrypt(ciphertext.encode()).decode()
