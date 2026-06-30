from pydantic import BaseModel
from typing import Optional, List

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
    tenant_id: str
    class Config:
        from_attributes = True

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

class InventoryDeductRequest(BaseModel):
    tenant_id: str
    branch_id: str
    product_id: int
    qty: int
