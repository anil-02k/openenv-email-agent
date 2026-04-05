from pydantic import BaseModel
from typing import List, Optional

class Email(BaseModel):
    id: int
    subject: str
    body: str
    priority: str  # low, medium, high

class Observation(BaseModel):
    emails: List[Email]
    processed: int
    correct: int

class Action(BaseModel):
    email_id: int
    action_type: str  # classify, reply, ignore
    response: Optional[str] = ""

class State(BaseModel):
    step_count: int
    total_reward: float