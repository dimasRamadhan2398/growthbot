from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List, Optional

import models
import schemas
from database import engine, Base, get_db

app = FastAPI(title="Tenant Service")

@app.on_event("startup")
def startup_db():
    Base.metadata.create_all(bind=engine)

def require_tenant_id(x_tenant_id: str = Header(None)):
    if not x_tenant_id:
        raise HTTPException(status_code=400, detail="X-Tenant-ID header missing")
    return x_tenant_id

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "tenant_service"}

@app.get("/api/tenants/validate/{subdomain}", response_model=schemas.TenantOut)
def validate_tenant_subdomain(subdomain: str, db: Session = Depends(get_db)):
    tenant = db.query(models.Tenant).filter(models.Tenant.subdomain == subdomain).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant

@app.get("/api/stores", response_model=List[schemas.StoreOut])
def get_stores(tenant_id: str = Depends(require_tenant_id), db: Session = Depends(get_db)):
    return db.query(models.Store).filter(models.Store.tenant_id == tenant_id).all()

# Internal endpoint for Order Service
@app.get("/api/internal/stores/{slug}", response_model=schemas.StoreOut)
def get_store_by_slug(slug: str, db: Session = Depends(get_db)):
    store = db.query(models.Store).filter(models.Store.slug == slug).first()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    return store

# Minimal dashboard mockup endpoint if needed
@app.get("/api/dashboard")
def get_dashboard(tenant_id: str = Depends(require_tenant_id), db: Session = Depends(get_db)):
    return {
        "tenant_id": tenant_id,
        "metrics": {"total_sales": "Rp 45.000.000", "total_orders": 128, "conversion_rate": "3.2%"},
        "chartData": [
            {"name": "Jan", "sales": 4000, "orders": 2400},
            {"name": "Feb", "sales": 3000, "orders": 1398},
            {"name": "Mar", "sales": 2000, "orders": 9800},
            {"name": "Apr", "sales": 2780, "orders": 3908},
            {"name": "May", "sales": 1890, "orders": 4800},
            {"name": "Jun", "sales": 2390, "orders": 3800},
        ],
        "recent_activity": [
            {"id": 1, "text": "New lead 'Budi' generated from Instagram", "time": "2 mins ago", "type": "lead"},
            {"id": 2, "text": "Order #ORD-001 shipped", "time": "1 hour ago", "type": "order"},
            {"id": 3, "text": "Product 'Premium T-Shirt' stock running low", "time": "3 hours ago", "type": "alert"},
        ]
    }

# Seed internal
@app.post("/api/internal/seed")
def seed_tenant(db: Session = Depends(get_db)):
    # Minimal seed for test
    if db.query(models.Tenant).count() == 0:
        tenant = models.Tenant(id="myfriedchicken", name="My Fried Chicken", subdomain="myfriedchicken", subscription_plan="pro", created_at="2026-06-29T00:00:00")
        db.add(tenant)
        branch = models.Branch(id="east-jakarta", tenant_id="myfriedchicken", name="East Jakarta")
        db.add(branch)
        outlet = models.Outlet(id="outlet-east-1", branch_id="east-jakarta", tenant_id="myfriedchicken", name="Outlet 1")
        db.add(outlet)
        store = models.Store(slug="mfc-id", tenant_id="myfriedchicken", name="MFC Store", owner="MFC", whatsapp="081234", tagline="Best chicken")
        db.add(store)
        db.commit()
    return {"status": "seeded"}
