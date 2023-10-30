from fastapi import FastAPI
from reactpy.backend.fastapi import configure
from reactpy import component, html
from fastapi.staticfiles import StaticFiles
from reactpy.core.hooks import create_context
from reactpy_router import route, simple

# Content
from screens.App import App
from screens.HistorialPedidos import HistorialPedidos
from screens.Inventarios import Inventarios
from screens.Ajustes import Ajustes

app = FastAPI()
app.mount("/CSS", StaticFiles(directory="CSS"), name="CSS")

############################################################
#API
from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import models
from database.database import engine, SessionLocal
from sqlalchemy.orm import Session

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
async def read_uniqueStock(stock_id: int, db:db_dependency):
        stock = db.query(models.Stock).filter(models.Stock.id == stock_id).first()
        if stock is None:
            HTTPException(status_code=404, detail='Stock not Found')
        return stock
    
@app.get("/stockfull", status_code=status.HTTP_200_OK)
async def read_fullStock(db:db_dependency):
        stocks = db.query(models.Stock).all()
        return stocks
############################################################    

@component
def Index():
    context = create_context("value")

    return simple.router(
        route("/", App(context)),
        route("/historial_de_pedidos", HistorialPedidos(context)),
        route("/inventarios",Inventarios(context)),  # Añade await aquí
        route("/ajustes", Ajustes(context))
    )

configure(app, Index)


configure(app, Index)