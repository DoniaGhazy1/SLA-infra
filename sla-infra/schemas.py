# api/schemas.py

from pydantic import BaseModel

class SlaRuleIn(BaseModel):
    bucket: str
    measurement: str
    field: str
    condition: str
    window: str
    severity: str

class SlaRuleOut(SlaRuleIn):
    id: int
    device_id: str

