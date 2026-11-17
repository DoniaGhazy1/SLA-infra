from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel
from typing import List
import json
import threading
import os

from config import SLA_POLICY_FILE

app = FastAPI(title="File-Backed SLA Policy API")
lock = threading.Lock()

# Input model: excludes device_id since it comes from path
class SlaRuleIn(BaseModel):
    bucket: str
    measurement: str
    field: str
    condition: str
    window: str
    severity: str

# Output model adds id and device_id
class SlaRuleOut(SlaRuleIn):
    id: int
    device_id: str


def _read_policies() -> List[dict]:
    if not os.path.exists(SLA_POLICY_FILE):
        return []
    with open(SLA_POLICY_FILE, "r") as f:
        return json.load(f)


def _write_policies(policies: List[dict]):
    with open(SLA_POLICY_FILE, "w") as f:
        json.dump(policies, f, indent=2)


@app.get("/devices/{device_id}/slas", response_model=List[SlaRuleOut])
def list_slas(device_id: str):
    policies = _read_policies()
    out = []
    for idx, p in enumerate(policies):
        if p.get("device_id") == device_id:
            out.append({**p, "id": idx})
    return out


@app.post("/devices/{device_id}/slas", response_model=SlaRuleOut, status_code=201)
def add_sla(device_id: str, payload: SlaRuleIn):
    with lock:
        policies = _read_policies()
        new = payload.dict()
        new["device_id"] = device_id
        policies.append(new)
        _write_policies(policies)
        idx = len(policies) - 1
    return {**new, "id": idx}


@app.put("/devices/{device_id}/slas/{sla_id}", response_model=SlaRuleOut)
def update_sla(
    device_id: str,
    sla_id: int = Path(..., ge=0),
    payload: SlaRuleIn = None
):
    with lock:
        policies = _read_policies()
        if sla_id >= len(policies) or policies[sla_id].get("device_id") != device_id:
            raise HTTPException(404, "SLA rule not found")
        updated = payload.dict()
        updated["device_id"] = device_id
        policies[sla_id] = updated
        _write_policies(policies)
    return {**updated, "id": sla_id}


@app.delete("/devices/{device_id}/slas/{sla_id}", status_code=204)
def delete_sla(device_id: str, sla_id: int = Path(..., ge=0)):
    with lock:
        policies = _read_policies()
        if sla_id >= len(policies) or policies[sla_id].get("device_id") != device_id:
            raise HTTPException(404, "SLA rule not found")
        policies.pop(sla_id)
        _write_policies(policies)
    return

