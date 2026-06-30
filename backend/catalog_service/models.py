from sqlalchemy import Column, Integer, String, Float, Boolean, Text
from database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(String, primary_key=True, index=True) # e.g., "Tops"
    tenant_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    icon = Column(String, nullable=True)
    webstore = Column(Boolean, default=True)
    reseller = Column(Boolean, default=True)
    pos = Column(Boolean, default=True)

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tenant_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    sku = Column(String, nullable=False, unique=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    online = Column(Integer, default=0)
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
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tenant_id = Column(String, nullable=False)
    branch_id = Column(String, nullable=False)
    outlet_id = Column(String, nullable=False)
    product_id = Column(Integer, nullable=False)
    stock = Column(Integer, default=0)
    online = Column(Integer, default=0)
