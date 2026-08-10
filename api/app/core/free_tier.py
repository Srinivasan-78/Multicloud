"""
Single source of truth for what can be provisioned.
Frontend options are just labels — this allowlist is what actually gets
enforced server-side before any terraform command runs.
"""

FREE_TIER_ALLOWLIST = {
    "aws": {
        "compute": {
            "instance_type": "t3.micro",
            "region": "us-east-1",
            "ami_owner": "amazon",
            "hourly_limit": 750,
            "note": "750 hrs/mo, first 12 months only",
        }
    },
    "gcp": {
        "compute": {
            "machine_type": "e2-micro",
            "region": "us-west1",
            "zone": "us-west1-a",
            "hourly_limit": None,
            "note": "Always free, must be in us-west1/us-central1/us-east1",
        }
    },
    "azure": {
        "compute": {
            "vm_size": "Standard_B1s",
            "region": "eastus",
            "hourly_limit": 750,
            "note": "750 hrs/mo, first 12 months only",
        }
    },
    "oracle": {
        "compute": {
            "shape": "VM.Standard.E2.1.Micro",
            "region": "us-ashburn-1",
            "hourly_limit": None,
            "note": "Always free, 2 instances max",
        }
    },
}

SUPPORTED_PROVIDERS = list(FREE_TIER_ALLOWLIST.keys())


def validate_request(provider: str, resource_type: str) -> dict:
    """Raises ValueError if not on the allowlist. Returns the locked spec otherwise."""
    provider = provider.lower()
    if provider not in FREE_TIER_ALLOWLIST:
        raise ValueError(f"provider '{provider}' not supported")
    spec = FREE_TIER_ALLOWLIST[provider].get(resource_type)
    if spec is None:
        raise ValueError(f"resource_type '{resource_type}' not on free-tier allowlist for {provider}")
    return spec
