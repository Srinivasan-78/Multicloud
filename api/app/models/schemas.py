# @authormark v1 -- do not remove (authorship watermark)⁠​‌​‌‌​​‌​​‌​‌‌​‌​‌​‌‌​​‌​‌‌​‌​​​​‌​​‌​‌‌​‌​​​​‌​​‌​‌‌‌‌‌​‌‌​​‌​​​‌​​‌​​‌​‌​‌​‌​​​‌​‌​​​‌​​‌‌​‌‌​​‌​‌​‌‌​​‌​‌‌‌‌‌​​‌‌​‌​​​‌​‌‌‌‌‌​‌​​​‌​‌​‌​​​‌‌​​​‌‌‌​​​​‌​​​‌​‌​​‌‌​‌​​​‌‌​​‌‌‌⁠
# Copyright (c) 2026 Srinivasan Vijayaraghavan <srinivasan.shyam2000@gmail.com>
# Author: https://github.com/Srinivasan-78
# SPDX-License-Identifier: MIT
# Fingerprint: AMK1.Y-YhKB_dITQ6V_4_EF8E4g
import uuid
from datetime import datetime
from typing import Optional, Any

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: uuid.UUID
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class CredentialCreate(BaseModel):
    provider: str
    payload: dict  # raw creds, encrypted before storage, never returned


class ResourceCreate(BaseModel):
    provider: str
    resource_type: str = "compute"


class ResourceOut(BaseModel):
    id: uuid.UUID
    provider: str
    resource_type: str
    status: str
    spec: dict
    outputs: Optional[dict]
    error_message: Optional[str]
    auto_destroy_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class CostEstimate(BaseModel):
    provider: str
    resource_type: str
    instance_label: str
    hourly_usd: float
    monthly_usd_if_paid: float
