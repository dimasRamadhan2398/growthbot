from sqlalchemy.orm import Session
import models
import datetime

def seed_data(db: Session):
    # Check if tenants exist to avoid reseeding
    if db.query(models.Tenant).first():
        return

    now = datetime.datetime.now().isoformat()

    # 1. Create Tenants
    tenant_fnb = models.Tenant(id="myfriedchicken", name="My Fried Chicken", subdomain="myfriedchicken", subscription_plan="pro", is_active=True, created_at=now)
    tenant_retail = models.Tenant(id="urbanstyle", name="Urban Style", subdomain="urbanstyle", subscription_plan="premium", is_active=True, created_at=now)
    tenant_service = models.Tenant(id="scbdpilates", name="SCBD Pilates", subdomain="scbdpilates", subscription_plan="basic", is_active=True, created_at=now)

    db.add_all([tenant_fnb, tenant_retail, tenant_service])
    db.commit()

    # 2. Create Branches
    branch_fnb_east = models.Branch(id="east-jakarta", tenant_id="myfriedchicken", name="East Jakarta", manager_name="Budi", region="DKI Jakarta", phone="08123456789")
    branch_retail_west = models.Branch(id="west-jakarta", tenant_id="urbanstyle", name="West Jakarta", manager_name="Siti", region="DKI Jakarta", phone="08129876543")
    branch_service_south = models.Branch(id="south-jakarta", tenant_id="scbdpilates", name="South Jakarta", manager_name="Andi", region="DKI Jakarta", phone="08121122334")

    db.add_all([branch_fnb_east, branch_retail_west, branch_service_south])
    db.commit()

    # 3. Create Outlets
    outlet_fnb_east = models.Outlet(id="outlet-east-1", branch_id="east-jakarta", tenant_id="myfriedchicken", name="Main Outlet East")
    outlet_retail_west = models.Outlet(id="outlet-west-1", branch_id="west-jakarta", tenant_id="urbanstyle", name="Main Outlet West")
    outlet_service_south = models.Outlet(id="outlet-south-1", branch_id="south-jakarta", tenant_id="scbdpilates", name="Main Outlet South")

    db.add_all([outlet_fnb_east, outlet_retail_west, outlet_service_south])
    db.commit()

    # 4. Create Categories
    categories = [
        models.Category(id="Tops", tenant_id="urbanstyle", name="Tops", icon="Shirt", webstore=True, reseller=True, pos=True),
        models.Category(id="Bottoms", tenant_id="urbanstyle", name="Bottoms", icon="ShoppingBag", webstore=True, reseller=True, pos=True),
        models.Category(id="Accessories", tenant_id="urbanstyle", name="Accessories", icon="Watch", webstore=True, reseller=True, pos=True),
        models.Category(id="Food", tenant_id="myfriedchicken", name="Food", icon="Pizza", webstore=True, reseller=True, pos=True),
        models.Category(id="Drinks", tenant_id="myfriedchicken", name="Drinks", icon="Coffee", webstore=True, reseller=True, pos=True),
        models.Category(id="Classes", tenant_id="scbdpilates", name="Classes", icon="Activity", webstore=True, reseller=True, pos=True),
    ]
    db.add_all(categories)
    db.commit()

    # 5. Create Stores
    stores = [
        models.Store(slug="urbanstyle-id", tenant_id="urbanstyle", name="Urban Style Official", owner="PT Urban Style", whatsapp="6281234567890", tagline="Your Daily Fashion", is_reseller=False, markup=0.0),
        models.Store(slug="myfriedchicken-id", tenant_id="myfriedchicken", name="My Fried Chicken Official", owner="PT Ayam Goreng", whatsapp="6281234567891", tagline="Crispy & Juicy", is_reseller=False, markup=0.0),
        models.Store(slug="scbdpilates-id", tenant_id="scbdpilates", name="SCBD Pilates Official", owner="PT Pilates Sehat", whatsapp="6281234567892", tagline="Strengthen Your Core", is_reseller=False, markup=0.0),
    ]
    db.add_all(stores)
    db.commit()

    # 6. Create Products
    products = [
        # Retail Products
        models.Product(tenant_id="urbanstyle", name="Classic White T-Shirt", sku="TSH-WHT-01", price=150000, category="Tops", status="synced", img="https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&q=80&w=800", rating=4.8, sold=1250, description="100% Cotton classic fit"),
        models.Product(tenant_id="urbanstyle", name="Vintage Denim Jacket", sku="JKT-DEN-01", price=450000, category="Tops", status="synced", img="https://images.unsplash.com/photo-1495105787522-5334e3ffa0ebd?auto=format&fit=crop&q=80&w=800", rating=4.9, sold=850, description="Premium vintage wash denim"),

        # FnB Products
        models.Product(tenant_id="myfriedchicken", name="Original Fried Chicken", sku="CHK-ORG-01", price=25000, category="Food", status="synced", img="https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?auto=format&fit=crop&q=80&w=800", rating=4.7, sold=5000, description="Crispy original recipe"),
        models.Product(tenant_id="myfriedchicken", name="Spicy Fried Chicken", sku="CHK-SPC-01", price=27000, category="Food", status="synced", img="https://images.unsplash.com/photo-1569691899455-88464f6d3ab1?auto=format&fit=crop&q=80&w=800", rating=4.8, sold=4500, description="Extra hot & spicy"),

        # Service Products
        models.Product(tenant_id="scbdpilates", name="Pilates Group Class", sku="CLS-GRP-01", price=200000, category="Classes", status="synced", img="https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&q=80&w=800", rating=4.9, sold=300, description="1 hour group session"),
    ]
    for p in products:
        db.add(p)
    db.commit()

    # 7. Create Inventory for Products
    # Re-fetch products to get IDs
    db_products = db.query(models.Product).all()
    inventories = []
    for p in db_products:
        if p.tenant_id == "urbanstyle":
            branch_id, outlet_id = "west-jakarta", "outlet-west-1"
        elif p.tenant_id == "myfriedchicken":
            branch_id, outlet_id = "east-jakarta", "outlet-east-1"
        else:
            branch_id, outlet_id = "south-jakarta", "outlet-south-1"

        inventories.append(models.Inventory(
            tenant_id=p.tenant_id,
            branch_id=branch_id,
            outlet_id=outlet_id,
            product_id=p.id,
            stock=100,
            online=50
        ))
    db.add_all(inventories)
    db.commit()

    # 8. Create Agents
    agents = [
        models.Agent(tenant_id="urbanstyle", name="Sales Assistant AI", status="active", messages=12543, channel="WhatsApp", icon_name="MessageSquare"),
        models.Agent(tenant_id="urbanstyle", name="Customer Support Bot", status="active", messages=8234, channel="Web Store", icon_name="Headphones"),
        models.Agent(tenant_id="myfriedchicken", name="Order Taker AI", status="active", messages=15430, channel="WhatsApp", icon_name="ShoppingBag"),
        models.Agent(tenant_id="scbdpilates", name="Booking Assistant", status="active", messages=3200, channel="Instagram", icon_name="HelpCircle"),
    ]
    db.add_all(agents)
    db.commit()

    # 9. Create Leads
    leads = [
        models.Lead(tenant_id="urbanstyle", name="Budi Santoso", initials="BS", source="Instagram Ads", value="Rp 2.5M", time="2 hours ago", column_name="New Lead"),
        models.Lead(tenant_id="urbanstyle", name="Siti Aminah", initials="SA", source="WhatsApp", value="Rp 1.2M", time="5 hours ago", column_name="Qualified by AI"),
        models.Lead(tenant_id="myfriedchicken", name="Andi Wijaya", initials="AW", source="TikTok", value="Rp 500k", time="1 day ago", column_name="In Discussion"),
        models.Lead(tenant_id="scbdpilates", name="Rina Melati", initials="RM", source="Website", value="Rp 3.5M", time="2 days ago", column_name="Closed"),
    ]
    db.add_all(leads)
    db.commit()

    print("Database seeded successfully with Multi-Tenant data!")
