from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.deps import get_current_user
from app.core.free_tier import validate_request, FREE_TIER_ALLOWLIST
from app.models.models import Resource, ResourceStatus, User
from app.models.schemas import ResourceCreate, ResourceOut, CostEstimate
from app.services import pricing
from app.services.tasks import provision_resource, destroy_resource
from app.core.config import settings

router = APIRouter(prefix="/resources", tags=["resources"])


@router.get("/catalog")
def catalog():
    """What's actually provisionable — drives the frontend dropdown."""
    return FREE_TIER_ALLOWLIST


@router.get("/catalog/estimate", response_model=list[CostEstimate])
def catalog_estimate():
    out = []
    for provider, types in FREE_TIER_ALLOWLIST.items():
        for rtype, spec in types.items():
            est = pricing.estimate(provider, rtype)
            out.append(
                CostEstimate(
                    provider=provider,
                    resource_type=rtype,
                    instance_label=spec.get("instance_type") or spec.get("machine_type")
                    or spec.get("vm_size") or spec.get("shape", ""),
                    hourly_usd=est["hourly_usd"],
                    monthly_usd_if_paid=est["monthly_usd_if_paid"],
                )
            )
    return out


@router.post("", response_model=ResourceOut, status_code=201)
def create_resource(
    payload: ResourceCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    try:
        spec = validate_request(payload.provider, payload.resource_type)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    existing_count = (
        db.query(Resource)
        .filter(
            Resource.user_id == user.id,
            Resource.provider == payload.provider,
            Resource.status.in_([ResourceStatus.pending, ResourceStatus.provisioning, ResourceStatus.active]),
        )
        .count()
    )
    if existing_count >= settings.max_resources_per_provider:
        raise HTTPException(
            status_code=429,
            detail=f"resource cap reached for {payload.provider} (max {settings.max_resources_per_provider})",
        )

    resource = Resource(
        user_id=user.id,
        provider=payload.provider,
        resource_type=payload.resource_type,
        status=ResourceStatus.pending,
        terraform_workspace=f"{user.id}/{payload.provider}",
        spec=spec,
    )
    db.add(resource)
    db.commit()
    db.refresh(resource)

    provision_resource.delay(str(resource.id))
    return resource


@router.get("", response_model=list[ResourceOut])
def list_resources(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Resource).filter(Resource.user_id == user.id).order_by(Resource.created_at.desc()).all()


@router.get("/{resource_id}", response_model=ResourceOut)
def get_resource(resource_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    resource = db.query(Resource).filter(Resource.id == resource_id, Resource.user_id == user.id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="not found")
    return resource


@router.delete("/{resource_id}", status_code=202)
def teardown_resource(resource_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    resource = db.query(Resource).filter(Resource.id == resource_id, Resource.user_id == user.id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="not found")
    destroy_resource.delay(str(resource.id))
    return {"status": "destroy_queued"}
