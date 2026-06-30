from pydantic import BaseModel
from typing import Optional, List

class TenantBase(BaseModel):
    id: str
    name: str
    subdomain: str
    subscription_plan: str
    is_active: bool = True
    created_at: str

class TenantCreate(TenantBase):
    pass

class TenantOut(TenantBase):
    class Config:
        from_attributes = True

class BranchBase(BaseModel):
    id: str
    tenant_id: str
    name: str
    manager_name: Optional[str] = None
    region: Optional[str] = None
    phone: Optional[str] = None

class BranchCreate(BranchBase):
    pass

class BranchOut(BranchBase):
    class Config:
        from_attributes = True

class OutletBase(BaseModel):
    id: str
    branch_id: str
    tenant_id: str
    name: str

class OutletCreate(OutletBase):
    pass

class OutletOut(OutletBase):
    class Config:
        from_attributes = True

class StoreBase(BaseModel):
    slug: str
    name: str
    owner: str
    logo: Optional[str] = None
    whatsapp: str
    tagline: str
    is_reseller: bool = False
    markup: float = 0.0

class StoreCreate(StoreBase):
    pass

class StoreOut(StoreBase):
    tenant_id: str
    class Config:
        from_attributes = True
