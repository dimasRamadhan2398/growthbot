from sqlalchemy.orm import Session
import models

def seed_data(db: Session):
    # 1. Seed Tenants
    if db.query(models.Tenant).count() == 0:
        tenants = [
            models.Tenant(
                id="urbanstyle",
                name="UrbanStyle Indonesia",
                subdomain="urbanstyle",
                subscription_plan="growth",
                is_active=True,
                created_at="2026-01-01T00:00:00"
            ),
            models.Tenant(
                id="tastybites",
                name="Tasty Bites Group",
                subdomain="tastybites",
                subscription_plan="enterprise",
                is_active=True,
                created_at="2026-01-01T00:00:00"
            )
        ]
        db.add_all(tenants)
        db.commit()
        print("Tenants seeded successfully!")

    # 2. Seed Branches
    if db.query(models.Branch).count() == 0:
        branches = [
            models.Branch(
                id="branch_retail_1",
                tenant_id="urbanstyle",
                name="UrbanStyle Senopati",
                manager_name="Andi Rahmawan",
                region="Jakarta Selatan",
                phone="6282222222222"
            ),
            models.Branch(
                id="branch_fnb_1",
                tenant_id="tastybites",
                name="Tasty Bites Sudirman",
                manager_name="Chef Juna",
                region="Jakarta Pusat",
                phone="6281111111111"
            )
        ]
        db.add_all(branches)
        db.commit()
        print("Branches seeded successfully!")

    # 3. Seed Outlets
    if db.query(models.Outlet).count() == 0:
        outlets = [
            models.Outlet(
                id="outlet_retail_1",
                branch_id="branch_retail_1",
                tenant_id="urbanstyle",
                name="Senopati Boutique Store"
            ),
            models.Outlet(
                id="outlet_fnb_1",
                branch_id="branch_fnb_1",
                tenant_id="tastybites",
                name="Sudirman Central Kitchen"
            )
        ]
        db.add_all(outlets)
        db.commit()
        print("Outlets seeded successfully!")

    # 4. Seed Categories
    if db.query(models.Category).count() == 0:
        categories = [
            # Retail (urbanstyle)
            models.Category(id="Tops", tenant_id="urbanstyle", name="Atasan", icon="👕", webstore=True, reseller=True, pos=True),
            models.Category(id="Bottoms", tenant_id="urbanstyle", name="Bawahan", icon="👖", webstore=True, reseller=True, pos=True),
            models.Category(id="Accessories", tenant_id="urbanstyle", name="Aksesoris", icon="🎒", webstore=True, reseller=True, pos=True),
            # FnB (tastybites)
            models.Category(id="Food", tenant_id="tastybites", name="Makanan", icon="🍔", webstore=True, reseller=False, pos=True),
            models.Category(id="Drinks", tenant_id="tastybites", name="Minuman", icon="🥤", webstore=True, reseller=False, pos=True),
        ]
        db.add_all(categories)
        db.commit()
        print("Categories seeded successfully!")

    # 5. Seed Stores
    if db.query(models.Store).count() == 0:
        stores = [
            # Retail
            models.Store(
                slug="urbanstyle-id",
                tenant_id="urbanstyle",
                name="UrbanStyle Indonesia",
                owner="Andi Rahmawan",
                whatsapp="6281234567890",
                tagline="Fashion streetwear berkualitas untuk semua.",
                is_reseller=False,
                markup=0.0
            ),
            models.Store(
                slug="dewa-fashion",
                tenant_id="urbanstyle",
                name="Dewa Fashion Corner",
                owner="Dewi Lestari",
                whatsapp="6281345678901",
                tagline="Pilihan fashion terbaik dari Dewa Fashion.",
                is_reseller=True,
                markup=15.0
            ),
            models.Store(
                slug="rudi-store",
                tenant_id="urbanstyle",
                name="Rudi's Collection",
                owner="Rudi Hermawan",
                whatsapp="6281456789012",
                tagline="Koleksi terkurasi untuk gaya Anda.",
                is_reseller=True,
                markup=10.0
            ),
            models.Store(
                slug="citra-boutique",
                tenant_id="urbanstyle",
                name="Citra Boutique",
                owner="Citra Kirana",
                whatsapp="6281567890123",
                tagline="Style premium, harga bersahabat.",
                is_reseller=True,
                markup=20.0
            ),
            # FnB
            models.Store(
                slug="tastybites-pos",
                tenant_id="tastybites",
                name="Tasty Bites Kitchen",
                owner="Chef Juna",
                whatsapp="6281111111111",
                tagline="Makanan lezat siap saji di Sudirman.",
                is_reseller=False,
                markup=0.0
            )
        ]
        db.add_all(stores)
        db.commit()
        print("Stores seeded successfully!")

    # 6. Seed Products
    if db.query(models.Product).count() == 0:
        products = [
            # Retail Products
            models.Product(
                id=1,
                tenant_id="urbanstyle",
                name="Kaos Polos Premium",
                sku="KPP-001",
                price=89000,
                status="synced",
                img="/products/product-kaos.png",
                rating=4.8,
                sold=1240,
                category="Tops",
                description="Kaos polos berbahan cotton combed 30s, nyaman dan adem dipakai sehari-hari.",
                ch_webstore=True,
                ch_reseller=True,
                ch_pos=True
            ),
            models.Product(
                id=2,
                tenant_id="urbanstyle",
                name="Tote Bag Canvas",
                sku="TBC-045",
                price=65000,
                status="synced",
                img="/products/product-totebag.png",
                rating=4.6,
                sold=890,
                category="Accessories",
                description="Tote bag kanvas tebal dengan tali kulit sintetis, cocok untuk daily use.",
                ch_webstore=True,
                ch_reseller=True,
                ch_pos=True
            ),
            models.Product(
                id=3,
                tenant_id="urbanstyle",
                name="Hoodie Oversize",
                sku="HOS-012",
                price=185000,
                status="synced",
                img="/products/product-hoodie.png",
                rating=4.9,
                sold=2100,
                category="Tops",
                description="Hoodie oversize bahan fleece premium, hangat dan stylish.",
                ch_webstore=True,
                ch_reseller=True,
                ch_pos=True
            ),
            models.Product(
                id=4,
                tenant_id="urbanstyle",
                name="Celana Jogger",
                sku="CJG-099",
                price=125000,
                status="synced",
                img="/products/product-jogger.png",
                rating=4.5,
                sold=760,
                category="Bottoms",
                description="Celana jogger bahan baby terry, elastis dan nyaman untuk aktivitas.",
                ch_webstore=True,
                ch_reseller=True,
                ch_pos=True
            ),
            models.Product(
                id=5,
                tenant_id="urbanstyle",
                name="Snapback Cap",
                sku="SBC-023",
                price=45000,
                status="synced",
                img="/products/product-cap.png",
                rating=4.3,
                sold=1580,
                category="Accessories",
                description="Topi snapback bahan premium dengan gesper logam adjustable.",
                ch_webstore=True,
                ch_reseller=True,
                ch_pos=True
            ),
            models.Product(
                id=6,
                tenant_id="urbanstyle",
                name="Kemeja Flanel",
                sku="KFL-077",
                price=149000,
                status="out",
                img="/products/product-flannel.png",
                rating=4.7,
                sold=430,
                category="Tops",
                description="Kemeja flanel kotak-kotak bahan katun tebal, cocok untuk outdoor.",
                ch_webstore=True,
                ch_reseller=True,
                ch_pos=True
            ),
            # FnB Products
            models.Product(
                id=7,
                tenant_id="tastybites",
                name="Nasi Goreng Special",
                sku="FNB-NGS",
                price=35000,
                status="synced",
                img="/products/product-nasigoreng.png",
                rating=4.8,
                sold=320,
                category="Food",
                description="Nasi goreng lezat dengan telur mata sapi dan ayam suwir.",
                ch_webstore=True,
                ch_reseller=False,
                ch_pos=True
            ),
            models.Product(
                id=8,
                tenant_id="tastybites",
                name="Es Teh Manis",
                sku="FNB-ETM",
                price=8000,
                status="synced",
                img="/products/product-esteh.png",
                rating=4.9,
                sold=850,
                category="Drinks",
                description="Es teh manis segar yang dibuat dengan gula asli.",
                ch_webstore=True,
                ch_reseller=False,
                ch_pos=True
            )
        ]
        db.add_all(products)
        db.commit()
        print("Products seeded successfully!")

    # 7. Seed Inventories
    if db.query(models.Inventory).count() == 0:
        inventories = [
            # Retail Inventories (for outlet_retail_1)
            models.Inventory(outlet_id="outlet_retail_1", product_id=1, stock=142, online_stock=138),
            models.Inventory(outlet_id="outlet_retail_1", product_id=2, stock=87, online_stock=87),
            models.Inventory(outlet_id="outlet_retail_1", product_id=3, stock=34, online_stock=31),
            models.Inventory(outlet_id="outlet_retail_1", product_id=4, stock=56, online_stock=56),
            models.Inventory(outlet_id="outlet_retail_1", product_id=5, stock=210, online_stock=208),
            models.Inventory(outlet_id="outlet_retail_1", product_id=6, stock=0, online_stock=0),
            # FnB Inventories (for outlet_fnb_1)
            models.Inventory(outlet_id="outlet_fnb_1", product_id=7, stock=50, online_stock=50),
            models.Inventory(outlet_id="outlet_fnb_1", product_id=8, stock=200, online_stock=200),
        ]
        db.add_all(inventories)
        db.commit()
        print("Inventories seeded successfully!")

    # 8. Seed Leads
    if db.query(models.Lead).count() == 0:
        leads = [
            # Retail Leads (urbanstyle)
            models.Lead(tenant_id="urbanstyle", name="Budi Santoso", initials="BS", source="WhatsApp", value="Rp 2.5M", time="10 min ago", column_name="New Lead"),
            models.Lead(tenant_id="urbanstyle", name="Sari Dewi", initials="SD", source="Shopee Chat", value="Rp 890K", time="25 min ago", column_name="New Lead"),
            models.Lead(tenant_id="urbanstyle", name="Rizki Pratama", initials="RP", source="TikTok", value="Rp 1.2M", time="1h ago", column_name="New Lead"),
            models.Lead(tenant_id="urbanstyle", name="Maya Putri", initials="MP", source="WhatsApp", value="Rp 5.8M", time="2h ago", column_name="Qualified by AI"),
            models.Lead(tenant_id="urbanstyle", name="Hendra Wijaya", initials="HW", source="Website", value="Rp 3.2M", time="3h ago", column_name="Qualified by AI"),
            models.Lead(tenant_id="urbanstyle", name="Tommy Liem", initials="TL", source="WhatsApp", value="Rp 12M", time="Yesterday", column_name="In Discussion"),
            models.Lead(tenant_id="urbanstyle", name="Fitri Handayani", initials="FH", source="Tokopedia", value="Rp 4.5M", time="Yesterday", column_name="In Discussion"),
            models.Lead(tenant_id="urbanstyle", name="Agus Setiawan", initials="AS", source="Walk-in", value="Rp 8.3M", time="2 days ago", column_name="In Discussion"),
            models.Lead(tenant_id="urbanstyle", name="Lina Marlina", initials="LM", source="WhatsApp", value="Rp 6.1M", time="3 days ago", column_name="Closed"),
            models.Lead(tenant_id="urbanstyle", name="Dedi Kurniawan", initials="DK", source="Shopee", value="Rp 2.9M", time="4 days ago", column_name="Closed"),
            # FnB Leads (tastybites)
            models.Lead(tenant_id="tastybites", name="Catering Permata", initials="CP", source="Website", value="Rp 15M", time="1h ago", column_name="New Lead"),
            models.Lead(tenant_id="tastybites", name="Aris Budiman", initials="AB", source="WhatsApp", value="Rp 3.5M", time="3h ago", column_name="Qualified by AI"),
        ]
        db.add_all(leads)
        db.commit()
        print("CRM Leads seeded successfully!")

    # 9. Seed Agents
    if db.query(models.Agent).count() == 0:
        agents = [
            # Retail Agents
            models.Agent(tenant_id="urbanstyle", name="WhatsApp Sales Assistant", status="active", messages=4820, channel="WhatsApp", icon_name="MessageSquare"),
            models.Agent(tenant_id="urbanstyle", name="Shopee Customer Support", status="active", messages=2310, channel="Shopee", icon_name="Headphones"),
            models.Agent(tenant_id="urbanstyle", name="Order Processing Bot", status="active", messages=1890, channel="Multi-channel", icon_name="ShoppingBag"),
            models.Agent(tenant_id="urbanstyle", name="FAQ Responder", status="active", messages=3140, channel="All Channels", icon_name="HelpCircle"),
            models.Agent(tenant_id="urbanstyle", name="TikTok Shop Assistant", status="paused", messages=780, channel="TikTok", icon_name="Package"),
            models.Agent(tenant_id="urbanstyle", name="Lead Qualifier", status="active", messages=1560, channel="WhatsApp", icon_name="Bot"),
            # FnB Agents
            models.Agent(tenant_id="tastybites", name="Tasty Bites Order Taker", status="active", messages=120, channel="WhatsApp", icon_name="ShoppingBag"),
            models.Agent(tenant_id="tastybites", name="Reservation Bot", status="active", messages=85, channel="Website", icon_name="Bot"),
        ]
        db.add_all(agents)
        db.commit()
        print("AI Agents seeded successfully!")

    # 10. Seed KB Files
    if db.query(models.KBFile).count() == 0:
        kb_files = [
            # Retail
            models.KBFile(tenant_id="urbanstyle", name="Product Catalog 2024.pdf", size="2.4 MB", date="Dec 12, 2025"),
            models.KBFile(tenant_id="urbanstyle", name="FAQ Database.xlsx", size="890 KB", date="Jan 5, 2026"),
            models.KBFile(tenant_id="urbanstyle", name="Shipping Policies.docx", size="156 KB", date="Mar 20, 2026"),
            models.KBFile(tenant_id="urbanstyle", name="Return & Refund Guide.pdf", size="1.1 MB", date="Apr 1, 2026"),
            # FnB
            models.KBFile(tenant_id="tastybites", name="Menu Catalog 2026.pdf", size="4.2 MB", date="May 10, 2026"),
            models.KBFile(tenant_id="tastybites", name="Hygiene & Safety Standards.pdf", size="1.5 MB", date="Jun 1, 2026"),
        ]
        db.add_all(kb_files)
        db.commit()
        print("Knowledge files seeded successfully!")

    # 11. Seed Orders
    if db.query(models.Order).count() == 0:
        # Retail Order 1
        ord1 = models.Order(
            id="ORD-2026041301",
            tenant_id="urbanstyle",
            branch_id="branch_retail_1",
            outlet_id="outlet_retail_1",
            store_name="UrbanStyle Indonesia",
            store_slug="urbanstyle-id",
            customer_name="Budi Santoso",
            customer_phone="081234567890",
            address="Jl. Sudirman No. 123, RT 01/RW 02, Kebayoran Baru",
            city="Jakarta Selatan, DKI Jakarta 12120",
            subtotal=363000,
            shipping_cost=15000,
            total=378000,
            shipping_method="GoSend Same Day",
            shipping_courier="Gojek",
            tracking_number="GK-2026041300123",
            payment_method="QRIS",
            payment_status="paid",
            status="out_for_delivery",
            estimated_delivery="13 Apr 2026, 18:00",
            created_at="2026-04-13T08:30:00"
        )
        db.add(ord1)
        db.flush()

        items1 = [
            models.OrderItem(order_id=ord1.id, product_id=1, qty=2, price=89000),
            models.OrderItem(order_id=ord1.id, product_id=3, qty=1, price=185000)
        ]
        events1 = [
            models.TrackingEvent(order_id=ord1.id, status="pending_payment", label="Pesanan Dibuat", description="Menunggu pembayaran via QRIS", timestamp="13 Apr 2026, 08:30"),
            models.TrackingEvent(order_id=ord1.id, status="paid", label="Pembayaran Diterima", description="Pembayaran QRIS berhasil diverifikasi", timestamp="13 Apr 2026, 08:32"),
            models.TrackingEvent(order_id=ord1.id, status="processing", label="Sedang Diproses", description="Penjual sedang menyiapkan pesanan Anda", timestamp="13 Apr 2026, 09:15", location="Gudang UrbanStyle, Jakarta"),
            models.TrackingEvent(order_id=ord1.id, status="shipped", label="Pesanan Dikirim", description="Paket diserahkan ke kurir GoSend", timestamp="13 Apr 2026, 10:45", location="Jakarta Selatan"),
            models.TrackingEvent(order_id=ord1.id, status="out_for_delivery", label="Sedang Diantar", description="Kurir sedang dalam perjalanan ke alamat Anda", timestamp="13 Apr 2026, 14:20", location="Kebayoran Baru, Jakarta Selatan")
        ]
        db.add_all(items1 + events1)

        # Retail Order 2
        ord2 = models.Order(
            id="ORD-2026041202",
            tenant_id="urbanstyle",
            branch_id="branch_retail_1",
            outlet_id="outlet_retail_1",
            store_name="UrbanStyle Indonesia",
            store_slug="urbanstyle-id",
            customer_name="Maya Putri",
            customer_phone="081345678901",
            address="Jl. Gatot Subroto No. 45, Menteng Dalam",
            city="Jakarta Selatan, DKI Jakarta 12870",
            subtotal=260000,
            shipping_cost=11000,
            total=271000,
            shipping_method="JNE Reguler (REG)",
            shipping_courier="JNE",
            tracking_number="JNE-1234567890",
            payment_method="Transfer Bank (VA)",
            payment_status="paid",
            status="in_transit",
            estimated_delivery="15 Apr 2026",
            created_at="2026-04-12T14:20:00"
        )
        db.add(ord2)
        db.flush()

        items2 = [
            models.OrderItem(order_id=ord2.id, product_id=5, qty=3, price=45000),
            models.OrderItem(order_id=ord2.id, product_id=4, qty=1, price=125000)
        ]
        events2 = [
            models.TrackingEvent(order_id=ord2.id, status="pending_payment", label="Pesanan Dibuat", description="Menunggu pembayaran via VA BCA", timestamp="12 Apr 2026, 14:20"),
            models.TrackingEvent(order_id=ord2.id, status="paid", label="Pembayaran Diterima", description="Transfer diterima via VA BCA", timestamp="12 Apr 2026, 14:35"),
            models.TrackingEvent(order_id=ord2.id, status="processing", label="Sedang Diproses", description="Pesanan sedang dikemas", timestamp="12 Apr 2026, 16:00", location="Gudang UrbanStyle, Jakarta"),
            models.TrackingEvent(order_id=ord2.id, status="shipped", label="Pesanan Dikirim", description="Paket diserahkan ke JNE", timestamp="12 Apr 2026, 17:30", location="JNE Jakarta"),
            models.TrackingEvent(order_id=ord2.id, status="in_transit", label="Dalam Perjalanan", description="Paket sedang dalam proses pengiriman", timestamp="13 Apr 2026, 06:00", location="JNE Hub Cakung, Jakarta")
        ]
        db.add_all(items2 + events2)

        # Retail Order 3 (Dewa Fashion is reseller storefront, markups applied)
        ord3 = models.Order(
            id="ORD-2026041103",
            tenant_id="urbanstyle",
            branch_id="branch_retail_1",
            outlet_id="outlet_retail_1",
            store_name="Dewa Fashion Corner",
            store_slug="dewa-fashion",
            customer_name="Rizki Pratama",
            customer_phone="081456789012",
            address="Jl. Diponegoro No. 78, Citarum",
            city="Bandung, Jawa Barat 40115",
            subtotal=425500,
            shipping_cost=10000,
            total=435500,
            shipping_method="SiCepat REG",
            shipping_courier="SiCepat",
            tracking_number="SCP-0098765432",
            payment_method="E-Wallet (GoPay)",
            payment_status="paid",
            status="delivered",
            estimated_delivery="13 Apr 2026",
            created_at="2026-04-11T10:00:00"
        )
        db.add(ord3)
        db.flush()

        items3 = [
            models.OrderItem(order_id=ord3.id, product_id=3, qty=2, price=212750)
        ]
        events3 = [
            models.TrackingEvent(order_id=ord3.id, status="pending_payment", label="Pesanan Dibuat", description="Menunggu pembayaran GoPay", timestamp="11 Apr 2026, 10:00"),
            models.TrackingEvent(order_id=ord3.id, status="paid", label="Pembayaran Diterima", description="Pembayaran GoPay berhasil", timestamp="11 Apr 2026, 10:02"),
            models.TrackingEvent(order_id=ord3.id, status="processing", label="Sedang Diproses", description="Pesanan sedang dikemas", timestamp="11 Apr 2026, 11:30", location="Gudang UrbanStyle, Jakarta"),
            models.TrackingEvent(order_id=ord3.id, status="shipped", label="Pesanan Dikirim", description="Paket diserahkan ke SiCepat", timestamp="11 Apr 2026, 14:00", location="SiCepat Jakarta"),
            models.TrackingEvent(order_id=ord3.id, status="in_transit", label="Dalam Perjalanan", description="Paket transit di hub sorting", timestamp="12 Apr 2026, 03:00", location="SiCepat Hub Karawang"),
            models.TrackingEvent(order_id=ord3.id, status="out_for_delivery", label="Sedang Diantar", description="Kurir menuju alamat penerima", timestamp="13 Apr 2026, 08:30", location="SiCepat Bandung"),
            models.TrackingEvent(order_id=ord3.id, status="delivered", label="Terkirim", description="Paket diterima oleh Rizki Pratama", timestamp="13 Apr 2026, 10:15", location="Bandung")
        ]
        db.add_all(items3 + events3)

        # FnB Order 1
        ord4 = models.Order(
            id="ORD-2026062501",
            tenant_id="tastybites",
            branch_id="branch_fnb_1",
            outlet_id="outlet_fnb_1",
            store_name="Tasty Bites Kitchen",
            store_slug="tastybites-pos",
            customer_name="Aris Budiman",
            customer_phone="081999888777",
            address="Gedung Artha Graha Lt. 12, Senayan",
            city="Jakarta Selatan, DKI Jakarta 12190",
            subtotal=78000,
            shipping_cost=15000,
            total=93000,
            shipping_method="GoSend Instant",
            shipping_courier="Gojek",
            tracking_number="GK-FNB-009988",
            payment_method="QRIS",
            payment_status="paid",
            status="delivered",
            estimated_delivery="25 Jun 2026, 14:00",
            created_at="2026-06-25T12:00:00"
        )
        db.add(ord4)
        db.flush()

        items4 = [
            models.OrderItem(order_id=ord4.id, product_id=7, qty=2, price=35000), # Nasi Goreng Special
            models.OrderItem(order_id=ord4.id, product_id=8, qty=1, price=8000),  # Es Teh Manis
        ]
        events4 = [
            models.TrackingEvent(order_id=ord4.id, status="pending_payment", label="Pesanan Dibuat", description="Menunggu pembayaran QRIS", timestamp="25 Jun 2026, 12:00"),
            models.TrackingEvent(order_id=ord4.id, status="paid", label="Pembayaran Diterima", description="Pembayaran QRIS terverifikasi", timestamp="25 Jun 2026, 12:02"),
            models.TrackingEvent(order_id=ord4.id, status="processing", label="Sedang Diproses", description="Kitchen sedang memasak pesanan Anda", timestamp="25 Jun 2026, 12:10", location="Central Kitchen Sudirman"),
            models.TrackingEvent(order_id=ord4.id, status="shipped", label="Pesanan Dikirim", description="Driver GoSend membawa pesanan Anda", timestamp="25 Jun 2026, 12:30", location="Jakarta Pusat"),
            models.TrackingEvent(order_id=ord4.id, status="delivered", label="Terkirim", description="Pesanan diterima oleh Aris Budiman", timestamp="25 Jun 2026, 12:45", location="Gedung Artha Graha")
        ]
        db.add_all(items4 + events4)

        db.commit()
        print("Orders seeded successfully!")
