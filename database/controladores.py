from fastapi import APIRouter, FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import models
from database.database import engine, SessionLocal
from sqlalchemy.orm import Session

router = APIRouter()

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
##Estas son algo así como las consultas a la base de datos, que se alojan en la ruta que marca, no son métodos que se llamen tal cual
@router.get("/stock/{stock_id}", status_code=status.HTTP_200_OK)
async def read_uniqueStock(stock_id: int, db:db_dependency):
        stock = db.query(models.Stock).filter(models.Stock.id == stock_id).first()
        if stock is None:
            HTTPException(status_code=404, detail='Stock not Found')
        return stock
    
@router.get("/stockfull", status_code=status.HTTP_200_OK)
async def read_fullStock(db:db_dependency):
        stocks = db.query(models.Stock).all()
        return stocks