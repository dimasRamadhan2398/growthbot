from pydantic import BaseModel
from typing import List, Optional

# --- Tenant ---
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

# --- Branch ---
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

# --- Outlet ---
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

# --- Category ---
class CategoryBase(BaseModel):
    id: str
    name: str
    icon: Optional[str] = None
    webstore: bool = True
    reseller: bool = True
    pos: bool = True

class CategoryCreate(CategoryBase):
    pass

class CategoryOut(CategoryBase):
    tenant_id: str
    class Config:
        from_attributes = True

# --- Store ---
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

# --- Product ---
class ProductBase(BaseModel):
    name: str
    sku: str
    price: float
    status: str = "synced"
    img: Optional[str] = None
    rating: float = 0.0
    sold: int = 0
    category: str
    description: Optional[str] = None
    ch_webstore: bool = True
    ch_reseller: bool = True
    ch_pos: bool = True

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    sku: Optional[str] = None
    price: Optional[float] = None
    status: Optional[str] = None
    img: Optional[str] = None
    rating: Optional[float] = None
    sold: Optional[int] = None
    category: Optional[str] = None
    description: Optional[str] = None
    ch_webstore: Optional[bool] = None
    ch_reseller: Optional[bool] = None
    ch_pos: Optional[bool] = None

class ProductOut(ProductBase):
    id: int
    tenant_id: str
    class Config:
        from_attributes = True

# --- Inventory ---
class InventoryBase(BaseModel):
    tenant_id: str
    branch_id: str
    outlet_id: str
    product_id: int
    stock: int = 0
    online: int = 0

class InventoryCreate(InventoryBase):
    pass

class InventoryOut(InventoryBase):
    id: int
    class Config:
        from_attributes = True

# --- Order Item ---
class OrderItemBase(BaseModel):
    product_id: int
    qty: int
    price: float

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemOut(OrderItemBase):
    id: int
    order_id: str
    class Config:
        from_attributes = True

# --- Tracking Event ---
class TrackingEventBase(BaseModel):
    status: str
    label: str
    description: str
    timestamp: str
    location: Optional[str] = None

class TrackingEventCreate(TrackingEventBase):
    pass

class TrackingEventOut(TrackingEventBase):
    id: int
    order_id: str
    class Config:
        from_attributes = True

# --- Order ---
class OrderBase(BaseModel):
    id: str
    store_name: str
    store_slug: str
    customer_name: str
    customer_phone: str
    address: str
    city: str
    subtotal: float
    shipping_cost: float
    total: float
    shipping_method: str
    shipping_courier: str
    tracking_number: Optional[str] = None
    payment_method: str
    payment_status: str = "pending"
    status: str = "pending_payment"
    estimated_delivery: Optional[str] = None
    created_at: str
    payment_url: Optional[str] = None
    payment_token: Optional[str] = None

class OrderCreate(BaseModel):
    store_slug: str
    customer_name: str
    customer_phone: str
    address: str
    city: str
    shipping_method: str
    shipping_courier: str
    shipping_cost: float
    payment_method: str
    items: List[OrderItemCreate]

class OrderUpdateStatus(BaseModel):
    status: str
    tracking_number: Optional[str] = None

class OrderOut(OrderBase):
    tenant_id: str
    branch_id: Optional[str] = None
    outlet_id: Optional[str] = None
    items: List[OrderItemOut] = []
    tracking_events: List[TrackingEventOut] = []
    class Config:
        from_attributes = True

# --- Lead CRM ---
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

# --- Agent ---
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

# --- KB File ---
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

# --- Logistics API ---
class ShippingRateRequest(BaseModel):
    city: str
    items: List[OrderItemCreate]

class ShippingOptionOut(BaseModel):
    id: str
    name: str
    courier: str
    type: str
    price: float
    eta: str
    popular: bool = False
