# @authormark v1 -- do not remove (authorship watermark)⁠​‌‌​​‌‌​​‌​​‌‌​​​‌‌​‌​‌​​‌​​​‌‌​​‌​‌​​​‌​‌​‌​‌‌​​‌​‌​​​​​‌‌‌​‌‌‌​‌‌​‌​‌​​‌‌‌​‌‌​​​‌​‌‌​‌​‌​​​​‌‌​‌​‌​​​‌​‌​​‌‌​​​​‌‌​‌‌​​​‌‌​​‌​​‌​‌​‌​‌​‌‌‌​​​​​​‌‌​​​‌​‌​​‌‌​‌​‌​‌​​‌​​‌​​​‌​​⁠
# Copyright (c) 2026 Srinivasan Vijayaraghavan <srinivasan.shyam2000@gmail.com>
# Author: https://github.com/Srinivasan-78
# SPDX-License-Identifier: MIT
# Fingerprint: AMK1.fLjFQVPwjv-CQL62Up1MRD
import enum
import uuid

from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, JSON, Boolean, func
from sqlalchemy.dialects.postgresql import UUID

from app.core.db import Base


class ResourceStatus(str, enum.Enum):
    pending = "pending"
    provisioning = "provisioning"
    active = "active"
    destroying = "destroying"
    destroyed = "destroyed"
    error = "error"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class CloudCredential(Base):
    __tablename__ = "cloud_credentials"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    provider = Column(String, nullable=False)  # aws | gcp | azure | oracle
    encrypted_payload = Column(String, nullable=False)  # fernet-encrypted JSON blob
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Resource(Base):
    __tablename__ = "resources"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    provider = Column(String, nullable=False)
    resource_type = Column(String, nullable=False)  # e.g. "compute"
    status = Column(Enum(ResourceStatus), default=ResourceStatus.pending, nullable=False)
    terraform_workspace = Column(String, nullable=False)
    spec = Column(JSON, nullable=False)  # locked free-tier spec used
    outputs = Column(JSON, nullable=True)  # resource_id, public_ip, etc.
    error_message = Column(String, nullable=True)
    auto_destroy_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class UsageLog(Base):
    __tablename__ = "usage_log"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resource_id = Column(UUID(as_uuid=True), ForeignKey("resources.id"), nullable=False)
    provider = Column(String, nullable=False)
    hours_active = Column(String, nullable=True)
    theoretical_cost_usd = Column(String, nullable=True)
    logged_at = Column(DateTime(timezone=True), server_default=func.now())
