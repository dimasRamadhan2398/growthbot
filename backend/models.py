from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base

class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(String, primary_key=True, index=True) # subdomain or unique ID
    name = Column(String, nullable=False)
    subdomain = Column(String, unique=True, index=True, nullable=False)
    subscription_plan = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(String, nullable=False)


class Branch(Base):
    __tablename__ = "branches"

    id = Column(String, primary_key=True, index=True)
    tenant_id = Column(String, ForeignKey("tenants.id"), nullable=False)
    name = Column(String, nullable=False)
    manager_name = Column(String, nullable=False)
    region = Column(String, nullable=False)
    phone = Column(String, nullable=False)


class Outlet(Base):
    __tablename__ = "outlets"

    id = Column(String, primary_key=True, index=True)
    branch_id = Column(String, ForeignKey("branches.id"), nullable=False)
    tenant_id = Column(String, ForeignKey("tenants.id"), nullable=False)
    name = Column(String, nullable=False)


class Category(Base):
    __tablename__ = "categories"

    id = Column(String, primary_key=True, index=True) # e.g., "Tops"
    tenant_id = Column(String, ForeignKey("tenants.id"), nullable=False)
    name = Column(String, nullable=False)
    icon = Column(String, nullable=True)
    webstore = Column(Boolean, default=True)
    reseller = Column(Boolean, default=True)
    pos = Column(Boolean, default=True)


class Store(Base):
    __tablename__ = "stores"

    slug = Column(String, primary_key=True, index=True) # e.g., "urbanstyle-id"
    tenant_id = Column(String, ForeignKey("tenants.id"), nullable=False)
    name = Column(String, nullable=False)
    owner = Column(String, nullable=False)
    logo = Column(String, nullable=True)
    whatsapp = Column(String, nullable=False)
    tagline = Column(String, nullable=False)
    is_reseller = Column(Boolean, default=False)
    markup = Column(Float, default=0.0)


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tenant_id = Column(String, ForeignKey("tenants.id"), nullable=False)
    name = Column(String, nullable=False)
    sku = Column(String, nullable=False, unique=True)
    price = Column(Float, nullable=False)
    status = Column(String, default="synced") # synced, syncing, out
    img = Column(Text, nullable=True) # base64 or URL or path
    rating = Column(Float, default=0.0)
    sold = Column(Integer, default=0)
    category = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    ch_webstore = Column(Boolean, default=True)
    ch_reseller = Column(Boolean, default=True)
    ch_pos = Column(Boolean, default=True)


class Inventory(Base):
    __tablename__ = "inventories"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    outlet_id = Column(String, ForeignKey("outlets.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    stock = Column(Integer, default=0)
    online_stock = Column(Integer, default=0)


class Order(Base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True, index=True) # e.g. ORD-2026041301
    tenant_id = Column(String, ForeignKey("tenants.id"), nullable=False)
    branch_id = Column(String, ForeignKey("branches.id"), nullable=True)
    outlet_id = Column(String, ForeignKey("outlets.id"), nullable=True)
    store_name = Column(String, nullable=False)
    store_slug = Column(String, nullable=False)
    customer_name = Column(String, nullable=False)
    customer_phone = Column(String, nullable=False)
    address = Column(Text, nullable=False)
    city = Column(String, nullable=False)
    subtotal = Column(Float, nullable=False)
    shipping_cost = Column(Float, nullable=False)
    total = Column(Float, nullable=False)
    shipping_method = Column(String, nullable=False)
    shipping_courier = Column(String, nullable=False)
    tracking_number = Column(String, nullable=True)
    payment_method = Column(String, nullable=False)
    payment_status = Column(String, default="pending") # pending, paid, expired, refunded
    status = Column(String, default="pending_payment") # pending_payment, paid, processing, shipped, etc.
    estimated_delivery = Column(String, nullable=True)
    created_at = Column(String, nullable=False)
    payment_url = Column(String, nullable=True)
    payment_token = Column(String, nullable=True)

    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    tracking_events = relationship("TrackingEvent", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(String, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, nullable=False)
    qty = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")


class TrackingEvent(Base):
    __tablename__ = "tracking_events"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(String, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    status = Column(String, nullable=False)
    label = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    timestamp = Column(String, nullable=False)
    location = Column(String, nullable=True)

    order = relationship("Order", back_populates="tracking_events")


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tenant_id = Column(String, ForeignKey("tenants.id"), nullable=False)
    name = Column(String, nullable=False)
    initials = Column(String, nullable=False)
    source = Column(String, nullable=False)
    value = Column(String, nullable=False) # e.g. Rp 2.5M
    time = Column(String, nullable=False)
    column_name = Column(String, nullable=False) # New Lead, Qualified by AI, In Discussion, Closed


class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tenant_id = Column(String, ForeignKey("tenants.id"), nullable=False)
    name = Column(String, nullable=False)
    status = Column(String, default="active") # active, paused
    messages = Column(Integer, default=0)
    channel = Column(String, nullable=False)
    icon_name = Column(String, nullable=False)


class KBFile(Base):
    __tablename__ = "kb_files"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tenant_id = Column(String, ForeignKey("tenants.id"), nullable=False)
    name = Column(String, nullable=False)
    size = Column(String, nullable=False)
    date = Column(String, nullable=False)
