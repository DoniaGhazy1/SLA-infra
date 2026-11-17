# api/crud.py

from sqlalchemy.orm import Session
from rules.model import SlaRule as SlaRuleModel  # your ORM model
from api.schemas import SlaRuleIn

def get_slas(db: Session, device_id: str):
    return db.query(SlaRuleModel).filter_by(device_id=device_id).all()

def create_sla(db: Session, device_id: str, payload: SlaRuleIn):
    sla = SlaRuleModel(device_id=device_id, **payload.dict())
    db.add(sla)
    db.commit()
    db.refresh(sla)
    return sla

def update_sla(db: Session, sla_id: int, device_id: str, payload: SlaRuleIn):
    sla = db.query(SlaRuleModel).filter_by(id=sla_id, device_id=device_id).first()
    if sla:
        for k, v in payload.dict().items():
            setattr(sla, k, v)
        db.commit()
    return sla

def delete_sla(db: Session, sla_id: int, device_id: str):
    deleted = db.query(SlaRuleModel).filter_by(id=sla_id, device_id=device_id).delete()
    db.commit()
    return deleted

