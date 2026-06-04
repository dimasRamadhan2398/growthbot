import datetime
import random
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from database import engine, Base, SessionLocal, get_db
from seed import seed_data
import models
import schemas

app = FastAPI(title="HumaiSpace AutoPilot API", version="1.0.0")

# Setup CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins for local development simplicity
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_data(db)
    except Exception as e:
        print(f"Error seeding database: {e}")
    finally:
        db.close()

# --- Health check ---
@app.get("/api/health")
def health_check():
    return {"status": "healthy", "time": datetime.datetime.utcnow().isoformat()}

# --- Dashboard API ---
@app.get("/api/dashboard")
def get_dashboard_data(db: Session = Depends(get_db)):
    # Calculate metrics
    agents_count = db.query(models.Agent).filter(models.Agent.status == "active").count()
    agents = db.query(models.Agent).all()
    total_messages = sum(a.messages for a in agents)

    # Let's count revenue from orders
    paid_orders = db.query(models.Order).filter(models.Order.payment_status == "paid").all()
    total_revenue = sum(o.total for o in paid_orders)
    
    # Human hours saved (mock calculation: 1 message = 3 minutes = 0.05 hours)
    hours_saved = int(total_messages * 0.05)

    metrics = [
        {"label": "Total Messages Automated", "value": f"{total_messages:,}", "change": "+12.5%", "icon": "MessageSquare", "color": "bg-primary/10 text-primary"},
        {"label": "Human Hours Saved", "value": f"{hours_saved:,}", "change": "+8.3%", "icon": "Clock", "color": "bg-success/10 text-success"},
        {"label": "Active AI Agents", "value": str(agents_count), "change": "+2", "icon": "Bot", "color": "bg-info/10 text-info"},
        {"label": "Revenue Influenced", "value": f"Rp {total_revenue / 1_000_000:.1f}M" if total_revenue >= 1_000_000 else f"Rp {total_revenue:,}", "change": "+23.1%", "icon": "TrendingUp", "color": "bg-warning/10 text-warning"}
    ]

    area_data = [
        {"month": "Jan", "messages": 2400, "leads": 120},
        {"month": "Feb", "messages": 3200, "leads": 180},
        {"month": "Mar", "messages": 2800, "leads": 160},
        {"month": "Apr", "messages": 4100, "leads": 240},
        {"month": "May", "messages": 5200, "leads": 310},
        {"month": "Jun", "messages": 4800, "leads": 290},
        {"month": "Jul", "messages": 6100, "leads": 380},
    ]

    channel_data = [
        {"channel": "WhatsApp", "value": 45},
        {"channel": "Shopee", "value": 22},
        {"channel": "Tokopedia", "value": 18},
        {"channel": "TikTok", "value": 15},
    ]

    agent_performance = []
    for a in agents:
        agent_performance.append({
            "name": a.name,
            "conversations": a.messages,
            "resolved": int(a.messages * random.uniform(0.90, 0.97))
        })

    return {
        "metrics": metrics,
        "areaData": area_data,
        "channelData": channel_data,
        "agentPerformance": agent_performance
    }

# --- Categories API ---
@app.get("/api/categories", response_model=List[schemas.CategoryOut])
def get_categories(db: Session = Depends(get_db)):
    return db.query(models.Category).all()

@app.post("/api/categories", response_model=schemas.CategoryOut)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    db_cat = db.query(models.Category).filter(models.Category.id == category.id).first()
    if db_cat:
        raise HTTPException(status_code=400, detail="Category ID already exists")
    new_cat = models.Category(**category.dict())
    db.add(new_cat)
    db.commit()
    db.refresh(new_cat)
    return new_cat

@app.delete("/api/categories/{cat_id}")
def delete_category(cat_id: str, db: Session = Depends(get_db)):
    db_cat = db.query(models.Category).filter(models.Category.id == cat_id).first()
    if not db_cat:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(db_cat)
    db.commit()
    return {"detail": "Category deleted successfully"}

# --- Products API ---
@app.get("/api/products", response_model=List[schemas.ProductOut])
def get_products(db: Session = Depends(get_db)):
    # Order by ID to keep consistent sorting
    return db.query(models.Product).order_by(models.Product.id.asc()).all()

@app.post("/api/products", response_model=schemas.ProductOut)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_prod = db.query(models.Product).filter(models.Product.sku == product.sku).first()
    if db_prod:
        raise HTTPException(status_code=400, detail="Product with this SKU already exists")
    new_prod = models.Product(**product.dict())
    db.add(new_prod)
    db.commit()
    db.refresh(new_prod)
    return new_prod

@app.put("/api/products/{product_id}", response_model=schemas.ProductOut)
def update_product(product_id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    db_prod = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_prod:
        raise HTTPException(status_code=404, detail="Product not found")
    
    update_data = product.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_prod, key, value)
    
    db.commit()
    db.refresh(db_prod)
    return db_prod

@app.delete("/api/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_prod = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_prod:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_prod)
    db.commit()
    return {"detail": "Product deleted successfully"}

# --- Stores API ---
@app.get("/api/stores", response_model=List[schemas.StoreOut])
def get_stores(db: Session = Depends(get_db)):
    return db.query(models.Store).all()

@app.get("/api/stores/{slug}", response_model=schemas.StoreOut)
def get_store_by_slug(slug: str, db: Session = Depends(get_db)):
    db_store = db.query(models.Store).filter(models.Store.slug == slug).first()
    if not db_store:
        raise HTTPException(status_code=404, detail="Store not found")
    return db_store

# --- Orders API ---
@app.get("/api/orders", response_model=List[schemas.OrderOut])
def get_orders(db: Session = Depends(get_db)):
    return db.query(models.Order).order_by(models.Order.created_at.desc()).all()

@app.get("/api/orders/{order_id}", response_model=schemas.OrderOut)
def get_order_by_id(order_id: str, db: Session = Depends(get_db)):
    db_order = db.query(models.Order).filter(
        (models.Order.id.ilike(order_id)) | 
        (models.Order.tracking_number.ilike(order_id))
    ).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@app.post("/api/orders", response_model=schemas.OrderOut)
def create_order(order_in: schemas.OrderCreate, db: Session = Depends(get_db)):
    # Retrieve store metadata
    db_store = db.query(models.Store).filter(models.Store.slug == order_in.store_slug).first()
    if not db_store:
        raise HTTPException(status_code=404, detail="Store not found")

    # Generate a unique Order ID
    order_id = f"ORD-{datetime.datetime.now().strftime('%Y%m%d')}{random.randint(10, 99)}"
    
    # Calculate subtotal, fetch prices
    subtotal = 0.0
    order_items = []
    
    for item in order_in.items:
        db_prod = db.query(models.Product).filter(models.Product.id == item.product_id).first()
        if not db_prod:
            raise HTTPException(status_code=400, detail=f"Product with ID {item.product_id} not found")
        
        # Calculate markup price if reseller storefront
        item_price = db_prod.price
        if db_store.is_reseller:
            item_price = round(db_prod.price * (1 + db_store.markup / 100))
        
        subtotal += item_price * item.qty
        
        # Deduct stock
        if db_prod.stock < item.qty:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for product: {db_prod.name}")
        db_prod.stock -= item.qty
        db_prod.online = max(0, db_prod.online - item.qty)
        if db_prod.stock <= 0:
            db_prod.status = "out"
        db_prod.sold += item.qty

        order_items.append(models.OrderItem(
            product_id=db_prod.id,
            qty=item.qty,
            price=item_price
        ))

    total = subtotal + order_in.shipping_cost

    # Payment Status & Order Status details
    # COD starts as paid/processing or pending? In COD, payment is pending. QRIS/VA is pending_payment.
    payment_status = "pending"
    order_status = "pending_payment"
    if order_in.payment_method == "COD (Bayar di Tempat)":
        order_status = "pending_payment"
        payment_status = "pending"

    # Set estimated delivery
    # Grab/GoSend = instant (1-2 hours)
    # JNE/J&T/SiCepat = 2-3 days
    now = datetime.datetime.now()
    if "instant" in order_in.shipping_method.lower() or "same day" in order_in.shipping_method.lower():
        est_delivery = (now + datetime.timedelta(hours=6)).strftime("%d %b %Y, %H:%M")
    else:
        est_delivery = (now + datetime.timedelta(days=3)).strftime("%d %b %Y")

    # ─── Payment Gateway API Integration Readiness ───
    # If the payment method is not COD, simulate/setup Xendit or Midtrans API integrations.
    payment_token = None
    payment_url = None
    if order_in.payment_method != "COD (Bayar di Tempat)":
        # Simulate a transaction token/invoice URL from payment gateway.
        # In a production environment, you would call Xendit or Midtrans API here:
        #
        # EXAMPLE MIDTRANS INTEGRATION:
        # import midtransclient
        # snap = midtransclient.Snap(is_production=False, server_key="YOUR_MIDTRANS_SERVER_KEY")
        # transaction = snap.create_transaction({
        #     "transaction_details": {
        #         "order_id": order_id,
        #         "gross_amount": int(total)
        #     },
        #     "customer_details": {
        #         "first_name": order_in.customer_name,
        #         "phone": order_in.customer_phone
        #     }
        # })
        # payment_token = transaction['token']
        # payment_url = transaction['redirect_url']
        #
        payment_token = f"snap-token-{order_id}-{random.randint(1000, 9999)}"
        payment_url = f"https://checkout.stripe.com/pay/mock-{order_id}"

    new_order = models.Order(
        id=order_id,
        store_name=db_store.name,
        store_slug=db_store.slug,
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
        estimated_delivery=est_delivery,
        created_at=now.isoformat(),
        payment_url=payment_url,
        payment_token=payment_token
    )

    db.add(new_order)
    db.flush()

    for oi in order_items:
        oi.order_id = new_order.id
        db.add(oi)

    # Add initial tracking event
    initial_event = models.TrackingEvent(
        order_id=new_order.id,
        status=order_status,
        label="Pesanan Dibuat",
        description=f"Pesanan berhasil dibuat. Menunggu konfirmasi pembayaran via {order_in.payment_method}.",
        timestamp=now.strftime("%d %b %Y, %H:%M")
    )
    db.add(initial_event)
    
    db.commit()
    db.refresh(new_order)
    return new_order

# --- Logistics API Rates Endpoint ---
@app.post("/api/shipping/rates", response_model=List[schemas.ShippingOptionOut])
def get_shipping_rates(req: schemas.ShippingRateRequest):
    # Calculate mock weight based on items (default 1 kg per item)
    total_qty = sum(item.qty for item in req.items)
    weight_grams = total_qty * 1000  # 1000g per item
    
    # In a production environment, you would call RajaOngkir or Biteship API here:
    #
    # EXAMPLE BITESHIP INTEGRATION:
    # import requests
    # url = "https://api.biteship.com/v1/rates"
    # headers = {"Authorization": "Bearer YOUR_BITESHIP_API_KEY", "Content-Type": "application/json"}
    # payload = {
    #     "origin_postal_code": "12120", # Gudang asal
    #     "destination_postal_code": "60234", # Kode pos pembeli
    #     "couriers": "jne,tiki,sicepat,gojek,grab",
    #     "items": [{"name": "Product Weight", "value": weight_grams, "quantity": 1}]
    # }
    # response = requests.post(url, json=payload, headers=headers).json()
    # ... map response to output format ...

    # We simulate rates based on the destination city string:
    is_jabodetabek = any(keyword in req.city.lower() for keyword in ["jakarta", "bogor", "depok", "tangerang", "bekasi", "jabar"])
    
    options = []
    
    if is_jabodetabek:
        # Offer local instant/sameday options
        options.append(schemas.ShippingOptionOut(id="gosend-instant", name="GoSend Instant", courier="Gojek", type="Instant", price=15000 + (weight_grams / 1000) * 5000, eta="1-2 jam", popular=True))
        options.append(schemas.ShippingOptionOut(id="grab-instant", name="GrabExpress Instant", courier="Grab", type="Instant", price=14000 + (weight_grams / 1000) * 5000, eta="1-2 jam"))
        options.append(schemas.ShippingOptionOut(id="gosend-sameday", name="GoSend Same Day", courier="Gojek", type="Same Day", price=10000 + (weight_grams / 1000) * 2000, eta="6-8 jam"))
        options.append(schemas.ShippingOptionOut(id="jne-reg", name="JNE Reguler (REG)", courier="JNE", type="Reguler", price=9000, eta="1-2 hari"))
        options.append(schemas.ShippingOptionOut(id="sicepat-reg", name="SiCepat REG", courier="SiCepat", type="Reguler", price=8000, eta="1-2 hari"))
    else:
        # Outside Jabodetabek, offer standard couriers only
        options.append(schemas.ShippingOptionOut(id="jne-reg", name="JNE Reguler (REG)", courier="JNE", type="Reguler", price=15000 + (weight_grams / 1000) * 3000, eta="2-3 hari", popular=True))
        options.append(schemas.ShippingOptionOut(id="jnt-ez", name="J&T Express EZ", courier="J&T", type="Reguler", price=14000 + (weight_grams / 1000) * 3000, eta="2-3 hari"))
        options.append(schemas.ShippingOptionOut(id="sicepat-reg", name="SiCepat REG", courier="SiCepat", type="Reguler", price=13000 + (weight_grams / 1000) * 3000, eta="2-3 hari"))
        options.append(schemas.ShippingOptionOut(id="jne-oke", name="JNE OKE (Ekonomi)", courier="JNE", type="Ekonomi", price=9000 + (weight_grams / 1000) * 2000, eta="3-5 hari"))

    return options

@app.put("/api/orders/{order_id}/status", response_model=schemas.OrderOut)
def update_order_status(order_id: str, status_update: schemas.OrderUpdateStatus, db: Session = Depends(get_db)):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    old_status = db_order.status
    db_order.status = status_update.status
    
    if status_update.tracking_number:
        db_order.tracking_number = status_update.tracking_number
    
    if status_update.status == "paid":
        db_order.payment_status = "paid"

    # Add tracking event
    labels = {
        "pending_payment": ("Pesanan Dibuat", "Menunggu konfirmasi pembayaran"),
        "paid": ("Pembayaran Diterima", "Pembayaran terverifikasi oleh sistem"),
        "processing": ("Sedang Diproses", "Penjual sedang menyiapkan pesanan Anda"),
        "shipped": ("Pesanan Dikirim", "Paket telah diserahkan ke kurir"),
        "in_transit": ("Dalam Perjalanan", "Paket sedang transit di pusat sorting"),
        "out_for_delivery": ("Sedang Diantar", "Kurir sedang dalam perjalanan ke alamat Anda"),
        "delivered": ("Terkirim", f"Paket berhasil diterima oleh {db_order.customer_name}"),
        "cancelled": ("Dibatalkan", "Pesanan telah dibatalkan oleh penjual/pembeli")
    }

    label, desc = labels.get(status_update.status, ("Status Update", f"Status updated from {old_status} to {status_update.status}"))
    
    now = datetime.datetime.now()
    new_event = models.TrackingEvent(
        order_id=db_order.id,
        status=status_update.status,
        label=label,
        description=desc,
        timestamp=now.strftime("%d %b %Y, %H:%M"),
        location="Gudang Utama" if status_update.status in ["processing", "shipped"] else None
    )
    db.add(new_event)
    
    db.commit()
    db.refresh(db_order)
    return db_order

# --- Leads API ---
@app.get("/api/leads", response_model=List[schemas.LeadOut])
def get_leads(db: Session = Depends(get_db)):
    return db.query(models.Lead).all()

@app.post("/api/leads", response_model=schemas.LeadOut)
def create_lead(lead: schemas.LeadCreate, db: Session = Depends(get_db)):
    new_lead = models.Lead(**lead.dict())
    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)
    return new_lead

@app.put("/api/leads/{lead_id}", response_model=schemas.LeadOut)
def update_lead(lead_id: int, lead_update: schemas.LeadUpdate, db: Session = Depends(get_db)):
    db_lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if not db_lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    if lead_update.column_name:
        db_lead.column_name = lead_update.column_name
    
    db.commit()
    db.refresh(db_lead)
    return db_lead

@app.delete("/api/leads/{lead_id}")
def delete_lead(lead_id: int, db: Session = Depends(get_db)):
    db_lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if not db_lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    db.delete(db_lead)
    db.commit()
    return {"detail": "Lead deleted successfully"}

# --- Agents API ---
@app.get("/api/agents", response_model=List[schemas.AgentOut])
def get_agents(db: Session = Depends(get_db)):
    return db.query(models.Agent).all()

@app.post("/api/agents", response_model=schemas.AgentOut)
def create_agent(agent: schemas.AgentCreate, db: Session = Depends(get_db)):
    new_agent = models.Agent(**agent.dict())
    db.add(new_agent)
    db.commit()
    db.refresh(new_agent)
    return new_agent

@app.put("/api/agents/{agent_id}", response_model=schemas.AgentOut)
def update_agent(agent_id: int, agent_update: schemas.AgentUpdate, db: Session = Depends(get_db)):
    db_agent = db.query(models.Agent).filter(models.Agent.id == agent_id).first()
    if not db_agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    if agent_update.status:
        db_agent.status = agent_update.status
    if agent_update.messages is not None:
        db_agent.messages = agent_update.messages
        
    db.commit()
    db.refresh(db_agent)
    return db_agent

# --- KB Files API ---
@app.get("/api/kb-files", response_model=List[schemas.KBFileOut])
def get_kb_files(db: Session = Depends(get_db)):
    return db.query(models.KBFile).all()

@app.post("/api/kb-files", response_model=schemas.KBFileOut)
def create_kb_file(kb_file: schemas.KBFileCreate, db: Session = Depends(get_db)):
    new_file = models.KBFile(**kb_file.dict())
    db.add(new_file)
    db.commit()
    db.refresh(new_file)
    return new_file

@app.delete("/api/kb-files/{file_id}")
def delete_kb_file(file_id: int, db: Session = Depends(get_db)):
    db_file = db.query(models.KBFile).filter(models.KBFile.id == file_id).first()
    if not db_file:
        raise HTTPException(status_code=404, detail="File metadata not found")
    db.delete(db_file)
    db.commit()
    return {"detail": "File deleted successfully"}
