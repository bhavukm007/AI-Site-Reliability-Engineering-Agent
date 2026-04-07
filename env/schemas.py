# env/schemas.py

from pydantic import BaseModel
from typing import List, Optional


# 🔹 OBSERVATION
class SREObservation(BaseModel):
    logs: str
    status: str


# 🔹 ACTION
class SREAction(BaseModel):
    action: str  # restart_db, scale_service, restart_service


# 🔹 STEP RESULT (IMPORTANT)
class SREResult(BaseModel):
    observation: SREObservation
    reward: float
    done: bool
    info: Optional[dict] = {}