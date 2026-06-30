from pydantic import BaseModel

class KBFileBase(BaseModel):
    name: str
    size: str
    date: str

class KBFileCreate(KBFileBase):
    pass

class KBFileOut(KBFileBase):
    id: int
    tenant_id: str
    class Config:
        from_attributes = True
