from database import SessionLocal
from models import DeliveryEvent


db = SessionLocal()

events = [
    {
        "supplierName": "Supplier A",
        "component": "Battery",
        "expectedDays": 4,
        "actualDays": 7,
        "status": "Delayed"
    },
    {
        "supplierName": "Supplier A",
        "component": "Battery",
        "expectedDays": 4,
        "actualDays": 6,
        "status": "Delayed"
    },
    {
        "supplierName": "Supplier A",
        "component": "Battery",
        "expectedDays": 4,
        "actualDays": 5,
        "status": "Delayed"
    },
    {
        "supplierName": "Supplier B",
        "component": "Display",
        "expectedDays": 3,
        "actualDays": 3,
        "status": "On Time"
    },
    {
        "supplierName": "Supplier B",
        "component": "Display",
        "expectedDays": 3,
        "actualDays": 4,
        "status": "Delayed"
    },
    {
        "supplierName": "Supplier C",
        "component": "RAM",
        "expectedDays": 5,
        "actualDays": 7,
        "status": "Delayed"
    },
    {
        "supplierName": "Supplier C",
        "component": "RAM",
        "expectedDays": 5,
        "actualDays": 5,
        "status": "On Time"
    },
    {
        "supplierName": "Supplier D",
        "component": "Processor",
        "expectedDays": 2,
        "actualDays": 2,
        "status": "On Time"
    }
]


for event in events:
    db.add(
        DeliveryEvent(
            supplierName=event["supplierName"],
            component=event["component"],
            expectedDays=event["expectedDays"],
            actualDays=event["actualDays"],
            status=event["status"]
        )
    )


db.commit()
db.close()

print("Delivery history added to database successfully.")