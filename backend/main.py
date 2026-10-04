from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base, SessionLocal
import models

app = FastAPI()
Base.metadata.create_all(bind=engine)


def initialize_database():
    db = SessionLocal()

    try:
        if db.query(models.Supplier).count() == 0:
            db.add_all([
                models.Supplier(name="Supplier A", component="Battery", deliveryDelay=6, inventoryDays=3, risk="High"),
                models.Supplier(name="Supplier B", component="Display", deliveryDelay=2, inventoryDays=12, risk="Low"),
                models.Supplier(name="Supplier C", component="RAM", deliveryDelay=4, inventoryDays=7, risk="Medium"),
                models.Supplier(name="Supplier D", component="Processor", deliveryDelay=1, inventoryDays=15, risk="Low")
            ])

        if db.query(models.Product).count() == 0:
            db.add_all([
                models.Product(name="Laptop Pro", components="Battery, Display, RAM, Processor", productionPerDay=500),
                models.Product(name="Laptop Air", components="Battery, Display, RAM, Processor", productionPerDay=300),
                models.Product(name="Business Laptop", components="Battery, Display, RAM, Processor", productionPerDay=200)
            ])

        if db.query(models.DeliveryEvent).count() == 0:
            db.add_all([
                models.DeliveryEvent(supplierName="Supplier A", component="Battery", expectedDays=4, actualDays=7, status="Delayed"),
                models.DeliveryEvent(supplierName="Supplier A", component="Battery", expectedDays=4, actualDays=6, status="Delayed"),
                models.DeliveryEvent(supplierName="Supplier A", component="Battery", expectedDays=4, actualDays=5, status="Delayed"),
                models.DeliveryEvent(supplierName="Supplier B", component="Display", expectedDays=3, actualDays=3, status="On Time"),
                models.DeliveryEvent(supplierName="Supplier B", component="Display", expectedDays=3, actualDays=4, status="Delayed"),
                models.DeliveryEvent(supplierName="Supplier C", component="RAM", expectedDays=5, actualDays=7, status="Delayed"),
                models.DeliveryEvent(supplierName="Supplier C", component="RAM", expectedDays=5, actualDays=5, status="On Time"),
                models.DeliveryEvent(supplierName="Supplier D", component="Processor", expectedDays=2, actualDays=2, status="On Time")
            ])

        db.commit()
    finally:
        db.close()


initialize_database()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "message": "TEAM ATLAS backend is running"
    }
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
products = [
    {
        "name": "Laptop Pro",
        "components": ["Battery", "Display", "RAM", "Processor"],
        "productionPerDay": 500
    },
    {
        "name": "Laptop Air",
        "components": ["Battery", "Display", "RAM", "Processor"],
        "productionPerDay": 300
    },
    {
        "name": "Business Laptop",
        "components": ["Battery", "Display", "RAM", "Processor"],
        "productionPerDay": 200
    }
]
@app.get("/suppliers")
def get_suppliers():
    db = SessionLocal()

    suppliers_from_db = db.query(models.Supplier).all()

    result = []

    for supplier in suppliers_from_db:
        result.append({
            "name": supplier.name,
            "component": supplier.component,
            "deliveryDelay": supplier.deliveryDelay,
            "inventoryDays": supplier.inventoryDays,
            "risk": supplier.risk
        })

    db.close()

    return result
@app.get("/products")
def get_products():
    db = SessionLocal()

    products_from_db = db.query(models.Product).all()

    result = []

    for product in products_from_db:
        result.append({
            "name": product.name,
            "components": product.components.split(", "),
            "productionPerDay": product.productionPerDay
        })

    db.close()

    return result

def calculate_risk_score(supplier):
    delay_risk = supplier["deliveryDelay"] * 10
    inventory_risk = max(0, 20 - supplier["inventoryDays"])

    score = min(100, delay_risk + inventory_risk)

    return score
def calculate_overall_risk_score(current_score, historical_score):
    overall_score = (
        current_score * 0.6
        + historical_score * 0.4
    )
    return round(overall_score, 2)

def generate_risk_explanation(supplier, historical_score, overall_score):

    if overall_score >= 60:
        level = "High"
    elif overall_score >= 30:
        level = "Medium"
    else:
        level = "Low"

    return (
        f"{level} risk because current delivery delay is "
        f"{supplier['deliveryDelay']} days, inventory coverage is "
        f"{supplier['inventoryDays']} days, and historical risk score is "
        f"{historical_score}."
    )
@app.get("/risk-analysis")
def get_risk_analysis():
    db = SessionLocal()

    suppliers_from_db = db.query(models.Supplier).all()

    results = []

    for supplier_db in suppliers_from_db:

        supplier = {
            "name": supplier_db.name,
            "component": supplier_db.component,
            "deliveryDelay": supplier_db.deliveryDelay,
            "inventoryDays": supplier_db.inventoryDays,
            "risk": supplier_db.risk
        }
        score = calculate_risk_score(supplier)

        historical_data = get_historical_risk()

        historical_score = 0

        for item in historical_data:
            if item["supplierName"] == supplier["name"]:
                historical_score = item["historicalRiskScore"]
                break

        overall_score = calculate_overall_risk_score(
            score,
            historical_score
        )
        risk_explanation = generate_risk_explanation(
    supplier,
    historical_score,
    overall_score
)

        affected = get_affected_products(supplier)
        production_impact = calculate_production_impact(supplier)

        results.append({
            "name": supplier["name"],
            "component": supplier["component"],
            "deliveryDelay": supplier["deliveryDelay"],
            "inventoryDays": supplier["inventoryDays"],
            "riskScore": score,
            "historicalRiskScore": historical_score,
            "overallRiskScore": overall_score,
            "riskExplanation": risk_explanation,
            "riskLevel": (
    "High" if overall_score >= 60
    else "Medium" if overall_score >= 30
    else "Low"
),
            "affectedProducts": [product["name"] for product in affected],
            "productionImpact": production_impact
        })

    db.close()

    return results

def get_affected_products(supplier):
    db = SessionLocal()

    products_from_db = db.query(models.Product).all()

    affected_products = []

    for product in products_from_db:
        components = product.components.split(", ")

        if supplier["component"] in components:
            affected_products.append({
                "name": product.name,
                "components": components,
                "productionPerDay": product.productionPerDay
            })

    db.close()

    return affected_products

@app.get("/product-impact")
def get_product_impact():
    db = SessionLocal()

    suppliers_from_db = db.query(models.Supplier).all()

    results = []

    for supplier_db in suppliers_from_db:

        supplier = {
            "name": supplier_db.name,
            "component": supplier_db.component,
            "deliveryDelay": supplier_db.deliveryDelay,
            "inventoryDays": supplier_db.inventoryDays,
            "risk": supplier_db.risk
        }

        affected = get_affected_products(supplier)

        results.append({
            "supplier": supplier["name"],
            "component": supplier["component"],
            "affectedProducts": [product["name"] for product in affected]
        })

    db.close()

    return results

def calculate_production_impact(supplier):
    affected_products = get_affected_products(supplier)

    total = 0

    for product in affected_products:
        total += product["productionPerDay"]

    return total


@app.get("/production-impact")
def get_production_impact():
    db = SessionLocal()

    suppliers_from_db = db.query(models.Supplier).all()

    results = []

    for supplier_db in suppliers_from_db:

        supplier = {
            "name": supplier_db.name,
            "component": supplier_db.component,
            "deliveryDelay": supplier_db.deliveryDelay,
            "inventoryDays": supplier_db.inventoryDays,
            "risk": supplier_db.risk
        }

        impact = calculate_production_impact(supplier)

        results.append({
            "supplier": supplier["name"],
            "component": supplier["component"],
            "productionImpact": impact
        })

    db.close()

    return results

@app.get("/dashboard")
def get_dashboard():
    db = SessionLocal()

    suppliers_from_db = db.query(models.Supplier).all()
    products_from_db = db.query(models.Product).all()

    total_suppliers = len(suppliers_from_db)
    total_products = len(products_from_db)

    high_risk_suppliers = 0

    active_risks = 0

    highest_risk_supplier = None
    highest_risk_score = -1

    historical_data = get_historical_risk()

    for supplier_db in suppliers_from_db:

        supplier = {
            "name": supplier_db.name,
            "component": supplier_db.component,
            "deliveryDelay": supplier_db.deliveryDelay,
            "inventoryDays": supplier_db.inventoryDays,
            "risk": supplier_db.risk
        }

        current_score = calculate_risk_score(supplier)

        historical_score = 0

        for item in historical_data:
            if item["supplierName"] == supplier["name"]:
                historical_score = item["historicalRiskScore"]
                break

        overall_score = calculate_overall_risk_score(
            current_score,
            historical_score
        )
        if overall_score >= 60:
            high_risk_suppliers += 1

        if overall_score > highest_risk_score:
            highest_risk_score = overall_score
            highest_risk_supplier = supplier["name"]

        if overall_score >= 50:
            active_risks += 1

    db.close()

    return {
        "totalSuppliers": total_suppliers,
        "totalProducts": total_products,
        "highRiskSuppliers": high_risk_suppliers,
        "activeRisks": active_risks,
        "highestRiskSupplier": highest_risk_supplier,
        "highestRiskScore": highest_risk_score
    }
@app.get("/simulation")
def get_simulation():
    db = SessionLocal()

    supplier_db = db.query(models.Supplier).first()

    supplier = {
        "name": supplier_db.name,
        "component": supplier_db.component,
        "deliveryDelay": supplier_db.deliveryDelay,
        "inventoryDays": supplier_db.inventoryDays,
        "risk": supplier_db.risk
    }

    production_impact = calculate_production_impact(supplier)

    current_score = calculate_risk_score(supplier)

    historical_data = get_historical_risk()

    historical_score = 0

    for item in historical_data:
        if item["supplierName"] == supplier["name"]:
            historical_score = item["historicalRiskScore"]
            break

    overall_score = calculate_overall_risk_score(
        current_score,
        historical_score
    )

    disruption_days = 10

    shortage_days = max(
        0,
        disruption_days - supplier["inventoryDays"]
    )

    expected_shortage = shortage_days * production_impact

    affected_products = len(
        get_affected_products(supplier)
    )

    db.close()

    return {
        "supplier": supplier["name"],
        "component": supplier["component"],
        "disruptionDays": disruption_days,
        "inventoryDays": supplier["inventoryDays"],
        "productionImpact": production_impact,
        "expectedShortage": expected_shortage,
        "affectedProducts": affected_products,
        "riskLevel": (
            "High" if overall_score >= 60
            else "Medium" if overall_score >= 30
            else "Low"
        )
    }
@app.get("/simulation/mitigation")
def get_mitigation_simulation():
    db = SessionLocal()

    supplier_db = db.query(models.Supplier).first()

    supplier = {
        "name": supplier_db.name,
        "component": supplier_db.component,
        "deliveryDelay": supplier_db.deliveryDelay,
        "inventoryDays": supplier_db.inventoryDays,
        "risk": supplier_db.risk
    }

    affected_products = get_affected_products(supplier)

    db.close()

    return {
        "alternativeSupplier": "Backup Battery Supplier",
        "component": supplier["component"],
        "supplyRestored": True,
        "expectedShortage": 0,
        "affectedProducts": 0,
        "riskLevel": "Low",
        "previousRiskLevel": "High",
        "previousAffectedProducts": len(affected_products)
    }

@app.get("/delivery-history")
def get_delivery_history():
    db = SessionLocal()

    events = db.query(models.DeliveryEvent).all()

    results = []

    for event in events:
        results.append({
            "supplierName": event.supplierName,
            "component": event.component,
            "expectedDays": event.expectedDays,
            "actualDays": event.actualDays,
            "status": event.status
        })

    db.close()

    return results
@app.get("/supplier-reliability")
def get_supplier_reliability():
    db = SessionLocal()

    events = db.query(models.DeliveryEvent).all()

    supplier_data = {}

    for event in events:

        if event.supplierName not in supplier_data:
            supplier_data[event.supplierName] = {
                "component": event.component,
                "totalEvents": 0,
                "totalDelay": 0,
                "delayedEvents": 0
            }

        supplier_data[event.supplierName]["totalEvents"] += 1

        delay = max(
            0,
            event.actualDays - event.expectedDays
        )

        supplier_data[event.supplierName]["totalDelay"] += delay

        if event.status == "Delayed":
            supplier_data[event.supplierName]["delayedEvents"] += 1

    results = []

    for supplier_name, data in supplier_data.items():

        total_events = data["totalEvents"]

        average_delay = (
            data["totalDelay"] / total_events
            if total_events > 0
            else 0
        )

        delay_rate = (
            data["delayedEvents"] / total_events * 100
            if total_events > 0
            else 0
        )

        results.append({
            "supplierName": supplier_name,
            "component": data["component"],
            "totalEvents": total_events,
            "averageDelay": round(average_delay, 2),
            "delayRate": round(delay_rate, 2)
        })

    db.close()

    return results

@app.get("/historical-risk")
def get_historical_risk():
    db = SessionLocal()

    events = db.query(models.DeliveryEvent).all()

    supplier_data = {}

    for event in events:

        if event.supplierName not in supplier_data:
            supplier_data[event.supplierName] = {
                "component": event.component,
                "totalEvents": 0,
                "totalDelay": 0,
                "delayedEvents": 0
            }

        supplier_data[event.supplierName]["totalEvents"] += 1

        delay = max(
            0,
            event.actualDays - event.expectedDays
        )

        supplier_data[event.supplierName]["totalDelay"] += delay

        if event.status == "Delayed":
            supplier_data[event.supplierName]["delayedEvents"] += 1

    results = []

    for supplier_name, data in supplier_data.items():

        total_events = data["totalEvents"]

        average_delay = (
            data["totalDelay"] / total_events
            if total_events > 0
            else 0
        )

        delay_rate = (
            data["delayedEvents"] / total_events * 100
            if total_events > 0
            else 0
        )

        historical_score = min(
            40,
            round(
                (average_delay * 10) +
                (delay_rate * 0.2),
                2
            )
        )

        results.append({
            "supplierName": supplier_name,
            "component": data["component"],
            "averageDelay": round(average_delay, 2),
            "delayRate": round(delay_rate, 2),
            "historicalRiskScore": historical_score
        })

    db.close()

    return results

@app.get("/recommendations")
def get_recommendations():
    db = SessionLocal()

    suppliers_from_db = db.query(models.Supplier).all()

    recommendations = []

    historical_data = get_historical_risk()

    for supplier_db in suppliers_from_db:

        supplier = {
            "name": supplier_db.name,
            "component": supplier_db.component,
            "deliveryDelay": supplier_db.deliveryDelay,
            "inventoryDays": supplier_db.inventoryDays,
            "risk": supplier_db.risk
        }

        current_score = calculate_risk_score(supplier)

        historical_score = 0

        for item in historical_data:
            if item["supplierName"] == supplier["name"]:
                historical_score = item["historicalRiskScore"]
                break

        overall_score = calculate_overall_risk_score(
            current_score,
            historical_score
        )

        if overall_score >= 60:
            action = "Activate backup supplier and increase inventory coverage."
        elif overall_score >= 30:
            action = "Monitor supplier closely and prepare a backup option."
        else:
            action = "Continue normal monitoring."

        recommendations.append({
            "supplier": supplier["name"],
            "component": supplier["component"],
            "riskScore": overall_score,
            "recommendation": action
        })

    db.close()

    return recommendations