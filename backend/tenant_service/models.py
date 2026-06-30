from sqlalchemy import Column, String, Boolean, ForeignKey, Float
from database import Base

class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    subdomain = Column(String, unique=True, nullable=False)
    subscription_plan = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(String, nullable=False)

class Branch(Base):
    __tablename__ = "branches"

    id = Column(String, primary_key=True, index=True)
    tenant_id = Column(String, nullable=False) # In microservices, we might use logical FKs or keep true FKs if in same DB
    name = Column(String, nullable=False)
    manager_name = Column(String, nullable=True)
    region = Column(String, nullable=True)
    phone = Column(String, nullable=True)

class Outlet(Base):
    __tablename__ = "outlets"

    id = Column(String, primary_key=True, index=True)
    branch_id = Column(String, nullable=False)
    tenant_id = Column(String, nullable=False)
    name = Column(String, nullable=False)

class Store(Base):
    __tablename__ = "stores"

    slug = Column(String, primary_key=True, index=True)
    tenant_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    owner = Column(String, nullable=False)
    logo = Column(String, nullable=True)
    whatsapp = Column(String, nullable=False)
    tagline = Column(String, nullable=False)
    is_reseller = Column(Boolean, default=False)
    markup = Column(Float, default=0.0)
