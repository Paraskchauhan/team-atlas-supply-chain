from sqlalchemy import Column, Integer, String
from database import Base


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    component = Column(String)
    deliveryDelay = Column(Integer)
    inventoryDays = Column(Integer)
    risk = Column(String)


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    components = Column(String)
    productionPerDay = Column(Integer)


class DeliveryEvent(Base):
    __tablename__ = "delivery_events"

    id = Column(Integer, primary_key=True, index=True)
    supplierName = Column(String)
    component = Column(String)
    expectedDays = Column(Integer)
    actualDays = Column(Integer)
    status = Column(String)