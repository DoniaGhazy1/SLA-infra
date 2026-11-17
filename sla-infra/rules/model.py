# rules/model.py

from pydantic import BaseModel

class SlaRule(BaseModel):
    """
    One SLA rule for one KPI on one device.
    """
    id: int 
    device_id: str
    bucket: str
    measurement: str
    field: str
    condition: str   # e.g. "value <= 50"
    window: str      # e.g. "1h"
    severity: str
    

