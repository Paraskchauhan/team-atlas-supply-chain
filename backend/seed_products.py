from database import SessionLocal
from models import Product


db = SessionLocal()

products = [
    {
        "name": "Laptop Pro",
        "components": "Battery, Display, RAM, Processor",
        "productionPerDay": 500
    },
    {
        "name": "Laptop Air",
        "components": "Battery, Display, RAM, Processor",
        "productionPerDay": 300
    },
    {
        "name": "Business Laptop",
        "components": "Battery, Display, RAM, Processor",
        "productionPerDay": 200
    }
]


for product in products:
    db.add(
        Product(
            name=product["name"],
            components=product["components"],
            productionPerDay=product["productionPerDay"]
        )
    )


db.commit()
db.close()

print("Products added to database successfully.")