from sqlalchemy import Boolean, Column, Integer, String
from database.database import Base

class Stock(Base):
    __tablename__ = 'stock'
    
    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String(255))
    numParte = Column(String(255))
    currentStock = Column(Integer)
    maxVenta = Column(Integer)
    minVenta = Column(Integer)
    puntoMax = Column(Integer)
    puntoReorden = Column(Integer)
