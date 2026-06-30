import os
import requests
import random
import datetime
from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List, Optional

import models
import schemas
from database import engine, Base, get_db

app = FastAPI(title="Order Service")

TENANT_SERVICE_URL = os.getenv("TENANT_SERVICE_URL", "http://localhost:8001")
CATALOG_SERVICE_URL = os.getenv("CATALOG_SERVICE_URL", "http://localhost:8002")

@app.on_event("startup")
def startup_db():
    Base.metadata.create_all(bind=engine)

def require_headers(
    x_tenant_id: str = Header(None),
    x_branch_id: str = Header(None),
    x_outlet_id: str = Header(None)
):
    if not x_tenant_id:
        raise HTTPException(status_code=400, detail="X-Tenant-ID header missing")
    return {"tenant_id": x_tenant_id, "branch_id": x_branch_id, "outlet_id": x_outlet_id}

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "order_service"}

@app.get("/api/orders", response_model=List[schemas.OrderOut])
def get_orders(headers: dict = Depends(require_headers), db: Session = Depends(get_db)):
    return db.query(models.Order).filter(models.Order.tenant_id == headers["tenant_id"]).all()

@app.get("/api/orders/{order_id}", response_model=schemas.OrderOut)
def get_order(order_id: str, db: Session = Depends(get_db)):
    # Note: track order might be public, so tenant ID might not be enforced strictly on read if order_id is unguessable
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.post("/api/orders", response_model=schemas.OrderOut)
def create_order(order_in: schemas.OrderCreate, headers: dict = Depends(require_headers), db: Session = Depends(get_db)):
    tenant_id = headers["tenant_id"]
    branch_id = headers.get("branch_id")
    outlet_id = headers.get("outlet_id")

    if not branch_id:
        raise HTTPException(status_code=400, detail="branch_id is required to create an order")

    # Fetch store details from tenant service
    store_resp = requests.get(f"{TENANT_SERVICE_URL}/api/internal/stores/{order_in.store_slug}")
    if store_resp.status_code != 200:
        raise HTTPException(status_code=404, detail="Store not found in tenant service")
    store_data = store_resp.json()

    # Calculate Subtotal and Validate Products
    subtotal = 0.0
    for item in order_in.items:
        prod_resp = requests.get(f"{CATALOG_SERVICE_URL}/api/internal/products/{item.product_id}")
        if prod_resp.status_code != 200:
            raise HTTPException(status_code=404, detail=f"Product ID {item.product_id} not found in catalog service")
        product = prod_resp.json()
        subtotal += item.price * item.qty

        # Deduct Inventory
        deduct_req = {
            "tenant_id": tenant_id,
            "branch_id": branch_id,
            "product_id": item.product_id,
            "qty": item.qty
        }
        deduct_resp = requests.post(f"{CATALOG_SERVICE_URL}/api/internal/inventory/deduct", json=deduct_req)
        if deduct_resp.status_code != 200:
            raise HTTPException(status_code=400, detail=f"Insufficient inventory for product {item.product_id}")

    total = subtotal + order_in.shipping_cost

    # Mock payment
    payment_token = None
    payment_url = None
    order_status = "pending_payment"
    payment_status = "pending"

    order_id = f"ORD-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}-{random.randint(100, 999)}"

    if order_in.payment_method == "qris":
        payment_token = f"snap-token-{order_id}-{random.randint(1000, 9999)}"
        payment_url = f"https://checkout.stripe.com/pay/mock-{order_id}"

    new_order = models.Order(
        id=order_id,
        tenant_id=tenant_id,
        branch_id=branch_id,
        outlet_id=outlet_id,
        store_name=store_data["name"],
        store_slug=order_in.store_slug,
        customer_name=order_in.customer_name,
        customer_phone=order_in.customer_phone,
        address=order_in.address,
        city=order_in.city,
        subtotal=subtotal,
        shipping_cost=order_in.shipping_cost,
        total=total,
        shipping_method=order_in.shipping_method,
        shipping_courier=order_in.shipping_courier,
        payment_method=order_in.payment_method,
        payment_status=payment_status,
        status=order_status,
        created_at=datetime.datetime.now().isoformat(),
        payment_url=payment_url,
        payment_token=payment_token
    )
    db.add(new_order)
    db.commit()

    for item in order_in.items:
        oi = models.OrderItem(**item.dict(), order_id=new_order.id)
        db.add(oi)

    initial_event = models.TrackingEvent(
        order_id=new_order.id,
        status=order_status,
        label="Order Placed",
        description="Waiting for payment" if payment_status == "pending" else "Order is being processed",
        timestamp=datetime.datetime.now().isoformat()
    )
    db.add(initial_event)
    db.commit()
    db.refresh(new_order)

    return new_order

@app.post("/api/shipping/rates", response_model=List[schemas.ShippingOptionOut])
def get_shipping_rates(req: schemas.ShippingRateRequest):
    total_qty = sum(item.qty for item in req.items)
    weight_grams = total_qty * 1000
    is_jabodetabek = any(keyword in req.city.lower() for keyword in ["jakarta", "bogor", "depok", "tangerang", "bekasi", "jabar"])
    options = []

    if is_jabodetabek:
        options.append(schemas.ShippingOptionOut(id="gosend-instant", name="GoSend Instant", courier="Gojek", type="Instant", price=15000 + (weight_grams / 1000) * 5000, eta="1-2 jam", popular=True))
        options.append(schemas.ShippingOptionOut(id="grab-instant", name="GrabExpress Instant", courier="Grab", type="Instant", price=14000 + (weight_grams / 1000) * 5000, eta="1-2 jam"))
    else:
        options.append(schemas.ShippingOptionOut(id="jne-reg", name="JNE Reguler (REG)", courier="JNE", type="Reguler", price=15000 + (weight_grams / 1000) * 3000, eta="2-3 hari", popular=True))

    return options

@app.put("/api/orders/{order_id}/status", response_model=schemas.OrderOut)
def update_order_status(
    order_id: str,
    status_update: schemas.OrderUpdateStatus,
    headers: dict = Depends(require_headers),
    db: Session = Depends(get_db)
):
    db_order = db.query(models.Order).filter(models.Order.id == order_id, models.Order.tenant_id == headers["tenant_id"]).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    db_order.status = status_update.status
    if status_update.tracking_number:
        db_order.tracking_number = status_update.tracking_number

    # Add tracking event
    desc_map = {
        "paid": "Payment successful. Processing order.",
        "shipped": f"Order shipped via {db_order.shipping_courier}." + (f" Tracking: {status_update.tracking_number}" if status_update.tracking_number else ""),
        "delivered": "Order has been delivered."
    }

    new_event = models.TrackingEvent(
        order_id=db_order.id,
        status=status_update.status,
        label=status_update.status.replace("_", " ").title(),
        description=desc_map.get(status_update.status, "Status updated."),
        timestamp=datetime.datetime.now().isoformat()
    )
    db.add(new_event)

    if status_update.status == "paid":
        db_order.payment_status = "paid"

    db.commit()
    db.refresh(db_order)
    return db_order
