from pydantic import BaseModel
from typing import List, Optional

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
    class Config:
        from_attributes = True

# --- Product ---
class ProductBase(BaseModel):
    name: str
    sku: str
    price: float
    stock: int = 0
    online: int = 0
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
    stock: Optional[int] = None
    online: Optional[int] = None
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
