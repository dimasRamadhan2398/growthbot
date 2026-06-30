from pydantic import BaseModel
from typing import Optional

class LeadBase(BaseModel):
    name: str
    initials: str
    source: str
    value: str
    time: str
    column_name: str

class LeadCreate(LeadBase):
    pass

class LeadUpdate(BaseModel):
    column_name: Optional[str] = None

class LeadOut(LeadBase):
    id: int
    tenant_id: str
    class Config:
        from_attributes = True

class AgentBase(BaseModel):
    name: str
    status: str = "active"
    messages: int = 0
    channel: str
    icon_name: str

class AgentCreate(AgentBase):
    pass

class AgentUpdate(BaseModel):
    status: Optional[str] = None
    messages: Optional[int] = None

class AgentOut(AgentBase):
    id: int
    tenant_id: str
    class Config:
        from_attributes = True
