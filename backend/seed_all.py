import requests

def seed_all():
    print("Seeding Tenant Service...")
    res = requests.post("http://localhost:8000/api/internal/seed")
    print(res.status_code, res.text)

    # We might need to map catalog internal seed directly to port 8002
    # since Nginx doesn't route /api/internal/seed for catalog (only for tenant due to lack of specificity).
    # Let's hit the services directly via docker-compose exposed ports if needed,
    # but here we can just hit them via nginx if we update nginx conf or hit docker internal dns if running inside container.

    # We don't have python requests locally outside container easily if ports are not exposed.
    # Actually wait, we should run this inside one of the containers or expose ports.
    # We'll just provide the script.
    print("Seeding Catalog Service...")
    res = requests.post("http://catalog_service:8002/api/internal/seed")
    print(res.status_code, res.text)

if __name__ == "__main__":
    seed_all()
