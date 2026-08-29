# @authormark v1 -- do not remove (authorship watermark)⁠​‌​​​‌‌‌​‌​‌‌​​‌​‌‌​​‌​‌​‌‌​‌​‌​​‌‌​​​‌​​‌‌​​‌​‌​‌‌‌​​‌‌​‌​​‌‌‌‌​‌‌​‌‌‌​​‌​‌​‌‌​​‌‌​‌‌​​​‌​​​​​‌​‌‌​​‌‌‌​‌‌​​​​‌​‌​‌‌‌‌‌​‌‌​​‌‌‌​‌​‌‌​‌​​‌‌‌​​‌​​‌‌​‌​​‌​‌​​​‌‌‌​‌​​​‌‌‌​‌‌​​‌‌‌⁠
# Copyright (c) 2026 Srinivasan Vijayaraghavan <srinivasan.shyam2000@gmail.com>
# Author: https://github.com/Srinivasan-78
# SPDX-License-Identifier: MIT
# Fingerprint: AMK1.GYejbesOnVlAga_gZriGGg
from datetime import datetime, timedelta

from app.core.celery_app import celery_app
from app.core.config import settings
from app.core.db import SessionLocal
from app.core.security import decrypt_secret
from app.models.models import Resource, ResourceStatus, CloudCredential
from app.services import terraform_runner


def _get_credentials(db, user_id, provider) -> dict:
    cred = (
        db.query(CloudCredential)
        .filter(CloudCredential.user_id == user_id, CloudCredential.provider == provider)
        .first()
    )
    if not cred:
        raise ValueError(f"no stored credentials for provider '{provider}'")
    import json

    return json.loads(decrypt_secret(cred.encrypted_payload))


@celery_app.task(name="provision_resource")
def provision_resource(resource_id: str):
    db = SessionLocal()
    try:
        resource = db.query(Resource).filter(Resource.id == resource_id).first()
        if not resource:
            return
        resource.status = ResourceStatus.provisioning
        db.commit()

        try:
            creds = _get_credentials(db, resource.user_id, resource.provider)
            outputs = terraform_runner.apply(
                str(resource.user_id), resource.provider, resource.spec, creds
            )
            resource.outputs = outputs
            resource.status = ResourceStatus.active
            resource.auto_destroy_at = datetime.utcnow() + timedelta(hours=settings.auto_destroy_hours)
        except Exception as e:
            resource.status = ResourceStatus.error
            resource.error_message = str(e)[:2000]
        db.commit()
    finally:
        db.close()


@celery_app.task(name="destroy_resource")
def destroy_resource(resource_id: str):
    db = SessionLocal()
    try:
        resource = db.query(Resource).filter(Resource.id == resource_id).first()
        if not resource:
            return
        resource.status = ResourceStatus.destroying
        db.commit()
        try:
            creds = _get_credentials(db, resource.user_id, resource.provider)
            terraform_runner.destroy(str(resource.user_id), resource.provider, creds)
            resource.status = ResourceStatus.destroyed
        except Exception as e:
            resource.status = ResourceStatus.error
            resource.error_message = str(e)[:2000]
        db.commit()
    finally:
        db.close()


@celery_app.task(name="sweep_expired_resources")
def sweep_expired_resources():
    """Run on a schedule (e.g. hourly via celery beat) to auto-destroy
    anything past its free-tier safety window."""
    db = SessionLocal()
    try:
        now = datetime.utcnow()
        expired = (
            db.query(Resource)
            .filter(Resource.status == ResourceStatus.active, Resource.auto_destroy_at <= now)
            .all()
        )
        for r in expired:
            destroy_resource.delay(str(r.id))
    finally:
        db.close()
