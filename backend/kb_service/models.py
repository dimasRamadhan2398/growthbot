from sqlalchemy import Column, Integer, String
from database import Base

class KBFile(Base):
    __tablename__ = "kb_files"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tenant_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    size = Column(String, nullable=False)
    date = Column(String, nullable=False)
