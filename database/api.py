from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import models
from database.database import engine, SessionLocal
from sqlalchemy.orm import Session
from Index import app

models.Base.metadata.create_all(bind=engine)

class StockBase(BaseModel):
    descripcion:str
    numParte:str
    currentStock:int
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/stock/{stock_id}", status_code=status.HTTP_200_OK)
async def read_stock(stock_id: int, db:db_dependency):
        stock = db.query(models.Stock).filter(models.Stock.id == stock_id).first()
        if stock is None:
            HTTPException(status_code=404, detail='Stock not Found')
        return stock
    