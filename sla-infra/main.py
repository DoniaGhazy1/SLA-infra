# api/main.py

from fastapi import FastAPI, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from api.schemas import SlaRuleIn, SlaRuleOut
from api.crud import get_slas, create_sla, update_sla, delete_sla
from config import DEVICE_ID
from api.dependencies import get_db  # your DB session provider

app = FastAPI(title="Device SLA Management")

@app.get("/devices/{device_id}/slas", response_model=list[SlaRuleOut])
def list_slas(device_id: str, db: Session = Depends(get_db)):
    return get_slas(db, device_id)

@app.post("/devices/{device_id}/slas", response_model=SlaRuleOut)
def add_sla(device_id: str, payload: SlaRuleIn, db: Session = Depends(get_db)):
    return create_sla(db, device_id, payload)

@app.put("/devices/{device_id}/slas/{sla_id}", response_model=SlaRuleOut)
def edit_sla(
    device_id: str,
    sla_id: int = Path(..., gt=0),
    payload: SlaRuleIn,
    db: Session = Depends(get_db)
):
    sla = update_sla(db, sla_id, device_id, payload)
    if not sla:
        raise HTTPException(404, "SLA not found")
    return sla

@app.delete("/devices/{device_id}/slas/{sla_id}", status_code=204)
def remove_sla(device_id: str, sla_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    count = delete_sla(db, sla_id, device_id)
    if not count:
        raise HTTPException(404, "SLA not found")

