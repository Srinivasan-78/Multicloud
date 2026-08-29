# @authormark v1 -- do not remove (authorship watermark)⁠​‌​​​‌​​​‌​​‌‌‌‌​‌‌​​‌‌​​​‌‌​​‌‌​‌​​​​‌​​‌‌​​‌​‌​​‌‌​​‌‌​‌‌​‌‌​‌​‌​​‌​‌‌​‌​​​​‌‌​‌‌​​‌​​​‌​‌​‌‌‌​‌‌‌​​‌‌​‌‌‌​​‌‌​‌‌​​​​‌​‌‌​​‌‌‌​‌​‌‌​‌​​‌​‌​​​​​‌‌‌​​​​​‌‌‌​​​‌​‌‌​​‌​​​‌​‌​​​​⁠
# Copyright (c) 2026 Srinivasan Vijayaraghavan <srinivasan.shyam2000@gmail.com>
# Author: https://github.com/Srinivasan-78
# SPDX-License-Identifier: MIT
# Fingerprint: AMK1.DOf3Be3mKCdWssagZPpqdP
import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.deps import get_current_user
from app.core.free_tier import SUPPORTED_PROVIDERS
from app.core.security import encrypt_secret
from app.models.models import CloudCredential, User
from app.models.schemas import CredentialCreate

router = APIRouter(prefix="/credentials", tags=["credentials"])


@router.post("", status_code=201)
def store_credential(
    payload: CredentialCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if payload.provider not in SUPPORTED_PROVIDERS:
        raise HTTPException(status_code=400, detail=f"unsupported provider '{payload.provider}'")

    existing = (
        db.query(CloudCredential)
        .filter(CloudCredential.user_id == user.id, CloudCredential.provider == payload.provider)
        .first()
    )
    encrypted = encrypt_secret(json.dumps(payload.payload))
    if existing:
        existing.encrypted_payload = encrypted
    else:
        db.add(CloudCredential(user_id=user.id, provider=payload.provider, encrypted_payload=encrypted))
    db.commit()
    return {"provider": payload.provider, "stored": True}


@router.get("")
def list_credentials(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # never return the encrypted payload itself
    rows = db.query(CloudCredential).filter(CloudCredential.user_id == user.id).all()
    return [{"provider": r.provider, "created_at": r.created_at} for r in rows]
