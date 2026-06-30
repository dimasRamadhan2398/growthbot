from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List, Optional

import models
import schemas
from database import engine, Base, get_db

app = FastAPI(title="Catalog Service")

@app.on_event("startup")
def startup_db():
    Base.metadata.create_all(bind=engine)

def require_tenant_id(x_tenant_id: str = Header(None)):
    if not x_tenant_id:
        raise HTTPException(status_code=400, detail="X-Tenant-ID header missing")
    return x_tenant_id

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "catalog_service"}

@app.get("/api/categories", response_model=List[schemas.CategoryOut])
def get_categories(tenant_id: str = Depends(require_tenant_id), db: Session = Depends(get_db)):
    return db.query(models.Category).filter(models.Category.tenant_id == tenant_id).all()

@app.post("/api/categories", response_model=schemas.CategoryOut)
def create_category(category: schemas.CategoryCreate, tenant_id: str = Depends(require_tenant_id), db: Session = Depends(get_db)):
    new_cat = models.Category(**category.dict(), tenant_id=tenant_id)
    db.add(new_cat)
    db.commit()
    db.refresh(new_cat)
    return new_cat

@app.get("/api/products", response_model=List[schemas.ProductOut])
def get_products(tenant_id: str = Depends(require_tenant_id), db: Session = Depends(get_db)):
    return db.query(models.Product).filter(models.Product.tenant_id == tenant_id).all()

@app.post("/api/products", response_model=schemas.ProductOut)
def create_product(product: schemas.ProductCreate, tenant_id: str = Depends(require_tenant_id), db: Session = Depends(get_db)):
    new_product = models.Product(**product.dict(), tenant_id=tenant_id)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@app.get("/api/products/{product_id}", response_model=schemas.ProductOut)
def get_product(product_id: int, tenant_id: str = Depends(require_tenant_id), db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id, models.Product.tenant_id == tenant_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.put("/api/products/{product_id}", response_model=schemas.ProductOut)
def update_product(product_id: int, product_update: schemas.ProductUpdate, tenant_id: str = Depends(require_tenant_id), db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id, models.Product.tenant_id == tenant_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    update_data = product_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

# Internal API for Order Service to deduct inventory
@app.post("/api/internal/inventory/deduct")
def deduct_inventory(req: schemas.InventoryDeductRequest, db: Session = Depends(get_db)):
    inv = db.query(models.Inventory).filter(
        models.Inventory.product_id == req.product_id,
        models.Inventory.branch_id == req.branch_id,
        models.Inventory.tenant_id == req.tenant_id
    ).first()

    if not inv or inv.stock < req.qty:
        raise HTTPException(status_code=400, detail=f"Insufficient branch stock for product {req.product_id}")

    inv.stock -= req.qty
    db.commit()
    return {"status": "success"}

# Internal API for Order Service to get product details
@app.get("/api/internal/products/{product_id}", response_model=schemas.ProductOut)
def internal_get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Seed internal
@app.post("/api/internal/seed")
def seed_catalog(db: Session = Depends(get_db)):
    if db.query(models.Category).count() == 0:
        cat = models.Category(id="Tops", name="Tops", tenant_id="myfriedchicken")
        db.add(cat)
        prod = models.Product(name="Fried Chicken Bucket", sku="FC-B-001", price=150000.0, stock=100, online=50, category="Tops", tenant_id="myfriedchicken")
        db.add(prod)
        db.commit()
        db.refresh(prod)
        inv = models.Inventory(tenant_id="myfriedchicken", branch_id="east-jakarta", outlet_id="outlet-east-1", product_id=prod.id, stock=100, online=50)
        db.add(inv)
        db.commit()
    return {"status": "seeded"}
