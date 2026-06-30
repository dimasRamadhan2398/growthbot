from sqlalchemy import Column, Integer, String
from database import Base

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tenant_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    initials = Column(String, nullable=False)
    source = Column(String, nullable=False)
    value = Column(String, nullable=False) # e.g. Rp 2.5M
    time = Column(String, nullable=False)
    column_name = Column(String, nullable=False)

class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tenant_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    status = Column(String, default="active")
    messages = Column(Integer, default=0)
    channel = Column(String, nullable=False)
    icon_name = Column(String, nullable=False)
