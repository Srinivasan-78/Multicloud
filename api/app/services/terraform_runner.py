# @authormark v1 -- do not remove (authorship watermark)⁠​‌‌​‌​​‌​‌​‌​​​‌​‌​‌​‌​‌​‌‌‌‌​​‌​‌‌‌​‌​​​‌‌​‌‌​‌​‌​​​​​‌​‌‌‌​​​‌​‌‌​‌​‌‌​‌​​​​​‌​‌‌​‌​​‌​‌​‌​‌‌​​‌‌‌​‌​‌​‌‌‌‌​​‌​‌​‌‌​‌​​‌‌​​‌‌​​‌‌​‌​‌​​‌‌​‌​​‌​​‌‌​‌​​​​‌‌​​​​​‌​‌​‌‌​​‌‌​​‌‌‌⁠
# Copyright (c) 2026 Srinivasan Vijayaraghavan <srinivasan.shyam2000@gmail.com>
# Author: https://github.com/Srinivasan-78
# SPDX-License-Identifier: MIT
# Fingerprint: AMK1.iQUytmAqkAiVuyZfji40Vg
import json
import os
import subprocess

from app.core.config import settings


class TerraformError(Exception):
    def __init__(self, message: str, stdout: str = "", stderr: str = ""):
        super().__init__(message)
        self.stdout = stdout
        self.stderr = stderr


def _workspace_dir(user_id: str, provider: str) -> str:
    path = os.path.join(settings.terraform_root, "tenants", str(user_id), provider)
    os.makedirs(path, exist_ok=True)
    return path


def _module_dir(provider: str) -> str:
    return os.path.join(settings.terraform_root, "modules", provider)


def _run(cmd: list[str], cwd: str) -> subprocess.CompletedProcess:
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=600)
    if result.returncode != 0:
        raise TerraformError(f"command failed: {' '.join(cmd)}", result.stdout, result.stderr)
    return result


def _write_tfvars(workspace: str, spec: dict, credentials: dict):
    tfvars = {**spec, **credentials}
    with open(os.path.join(workspace, "terraform.tfvars.json"), "w") as f:
        json.dump(tfvars, f)


def _ensure_main_tf_symlink(workspace: str, provider: str):
    """Symlink the module's .tf files into the tenant workspace so each tenant
    gets its own state dir without duplicating module source."""
    module_dir = _module_dir(provider)
    for fname in os.listdir(module_dir):
        if fname.endswith(".tf"):
            link = os.path.join(workspace, fname)
            target = os.path.join(module_dir, fname)
            if not os.path.islink(link) and not os.path.exists(link):
                os.symlink(target, link)


def apply(user_id: str, provider: str, spec: dict, credentials: dict) -> dict:
    workspace = _workspace_dir(user_id, provider)
    _ensure_main_tf_symlink(workspace, provider)
    _write_tfvars(workspace, spec, credentials)

    _run(["terraform", "init", "-input=false"], cwd=workspace)
    _run(["terraform", "apply", "-auto-approve", "-input=false"], cwd=workspace)
    output = _run(["terraform", "output", "-json"], cwd=workspace)
    return json.loads(output.stdout)


def destroy(user_id: str, provider: str, credentials: dict) -> None:
    workspace = _workspace_dir(user_id, provider)
    if not os.path.exists(os.path.join(workspace, "terraform.tfstate")):
        return  # nothing provisioned, nothing to destroy
    _write_tfvars(workspace, {}, credentials)
    _run(["terraform", "destroy", "-auto-approve", "-input=false"], cwd=workspace)
