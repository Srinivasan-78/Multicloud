# Multi-Cloud Free-Tier Platform (portfolio project)

A single dashboard that provisions compute on AWS, GCP, Azure, or Oracle Cloud —
strictly within each provider's free tier — via Terraform, with a unified
status view and theoretical cost comparison.

**This is a technical demonstration of multi-cloud platform engineering, not
a production billing/brokerage product.** See "Known limitations" below.

## Architecture

```
Frontend (Next.js) → API (FastAPI) → Celery worker → Terraform → AWS/GCP/Azure/Oracle
                           ↓                              ↓
                       Postgres                   per-tenant state
                (users, resources, creds)      /terraform/tenants/{user_id}/{provider}
```

- **API** validates every provisioning request against a hardcoded free-tier
  allowlist (`api/app/core/free_tier.py`) before any Terraform command runs —
  this check happens server-side regardless of what the frontend sends.
- **Celery worker** runs `terraform init/apply/destroy` as subprocesses, async,
  per-tenant workspace, so one user's state never touches another's.
- **Auto-destroy sweep** (Celery beat, hourly) tears down anything past its
  24h safety window to avoid orphaned free-tier resources.

## Repo layout

```
api/            FastAPI app, Celery tasks, SQLAlchemy models
terraform/
  modules/      One module per provider (aws, gcp implemented; azure/oracle stubs)
  tenants/      Per-user Terraform state, created at runtime
frontend/       Next.js dashboard
docker-compose.yml
```

## Running it

1. Copy `api/.env.example` → `api/.env`, fill in `JWT_SECRET` and generate a
   `FERNET_KEY`:
   ```
   python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
   ```
2. `docker compose up --build`
3. Frontend: http://localhost:3000 · API docs: http://localhost:8000/docs
4. Register a user, `POST /credentials` with your own cloud credentials
   (never committed, encrypted at rest with Fernet), then provision from
   the dashboard.

You need your own AWS/GCP accounts with free tier available — this app
provisions real (free-tier) resources on your accounts, it does not host
compute itself.

## Free-tier enforcement

Locked in `free_tier.py` and mirrored as Terraform variable validation
blocks (belt-and-suspenders — reject bad input at both the API layer and
inside the module itself):

| Provider | Instance | Region constraint | Window |
|---|---|---|---|
| AWS | t3.micro | us-east-1 | 750 hrs/mo, first 12 months |
| GCP | e2-micro | us-west1/us-central1/us-east1 | always free |
| Azure | Standard_B1s | eastus | 750 hrs/mo, first 12 months |
| Oracle | VM.Standard.E2.1.Micro | us-ashburn-1 | always free |

Resource cap: 1 active resource per provider per user
(`MAX_RESOURCES_PER_PROVIDER`), auto-destroyed after 24h
(`AUTO_DESTROY_HOURS`).

## Known limitations / what this is not

- **Not a real multi-cloud reseller.** Actually brokering paid usage across
  providers requires MSP/CSP partner agreements with each cloud (AWS, Azure,
  GCP, OCI), margin/billing infrastructure, and compliance review — this repo
  demonstrates the provisioning/orchestration layer only, using each user's
  own free-tier credentials.
- **Terraform state has no locking configured.** Each tenant/provider pair
  runs in its own directory so concurrent-apply risk is low for this demo,
  but a real deployment should use S3+DynamoDB or GCS native locking instead
  of local state files.
- **Cost dashboard is illustrative.** Hardcoded pricing snapshot
  (`services/pricing.py`), not a live pricing API call — real spend is $0 on
  free tier regardless.
- **Azure/Oracle modules are stubs** — same pattern as AWS/GCP, not yet
  implemented in this scaffold.
- **Credential storage** uses Fernet symmetric encryption with a single key
  in an env var — fine for a demo, not how you'd do tenant secret isolation
  in production (would want per-tenant KMS keys / a real secrets manager).
