from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True, index=True) # e.g. ORD-2026041301
    tenant_id = Column(String, nullable=False)
    branch_id = Column(String, nullable=True)
    outlet_id = Column(String, nullable=True)
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
    payment_status = Column(String, default="pending")
    status = Column(String, default="pending_payment")
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
