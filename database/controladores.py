from fastapi import APIRouter, HTTPException, Depends, status, Request
from typing import Annotated
import models
from database.database import engine, SessionLocal
from sqlalchemy.orm import Session

router = APIRouter()

models.DataBase.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

##Éstas son algo así como las consultas a la base de datos, que se alojan en la ruta que marca, no son métodos que se llamen tal cual
@router.get("/stock/{stock_id}", status_code=status.HTTP_200_OK)
async def read_uniqueStock(stock_id: int, db: db_dependency):
    stock = db.query(models.Productos).filter(models.Productos.id == stock_id).first()
    if stock is None:
        raise HTTPException(status_code=404, detail='Stock not Found')
    return stock

#Lee la tabla de productos, pai
@router.get("/stockfull", status_code=status.HTTP_200_OK)
async def read_fullStock(db: db_dependency):
    stocks = db.query(models.Productos).all()
    return stocks

#Este postea un pedido entrante con el formato JSON, las fechas y el id son el mismo, pero inserta múltiples registros por producto
@router.post("/pedidoEntrante", status_code=status.HTTP_201_CREATED)
async def create_pedido_entrante(request: Request, db: db_dependency):
    try:
        data = await request.json()
        for pedido_data in data:
            fecha_pedido = pedido_data["fecha_pedido"]
            fecha_entrega = pedido_data["fecha_entrega"]
            metodo_pago = pedido_data["metodo_pago"]
            for producto_data in pedido_data["productos"]:
                producto_id = producto_data["id"]
                cantidad = producto_data["cantidad"]
                nuevo_pedido = models.PedidoEntrante(
                    producto_id=producto_id,
                    fecha_pedido=fecha_pedido,
                    fecha_entrega=fecha_entrega,
                    cantidad=cantidad,
                    metodo_pago=metodo_pago
                )
                db.add(nuevo_pedido)
                db.commit()
        return {"message": "Pedidos entrantes creados exitosamente, perro!"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/backend/pedidosEntrantes", status_code=status.HTTP_200_OK)
async def read_pedidosEntrantes(db: db_dependency):
    pedidos = db.query(models.PedidoEntrante).all()
    return pedidos