from database import SessionLocal
from models import Supplier


db = SessionLocal()

suppliers = [
    {
        "name": "Supplier A",
        "component": "Battery",
        "deliveryDelay": 6,
        "inventoryDays": 3,
        "risk": "High"
    },
    {
        "name": "Supplier B",
        "component": "Display",
        "deliveryDelay": 2,
        "inventoryDays": 12,
        "risk": "Low"
    },
    {
        "name": "Supplier C",
        "component": "RAM",
        "deliveryDelay": 4,
        "inventoryDays": 7,
        "risk": "Medium"
    },
    {
        "name": "Supplier D",
        "component": "Processor",
        "deliveryDelay": 1,
        "inventoryDays": 15,
        "risk": "Low"
    }
]


for supplier in suppliers:
    db.add(
        Supplier(
            name=supplier["name"],
            component=supplier["component"],
            deliveryDelay=supplier["deliveryDelay"],
            inventoryDays=supplier["inventoryDays"],
            risk=supplier["risk"]
        )
    )


db.commit()
db.close()

print("Suppliers added to database successfully.")