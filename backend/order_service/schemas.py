from pydantic import BaseModel
from typing import Optional, List

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
