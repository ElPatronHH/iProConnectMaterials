from fastapi import APIRouter, HTTPException, Depends, status, Request
from typing import Annotated
from pydantic import BaseModel
import models
from database.database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy.orm import aliased
from sqlalchemy import select, join

router = APIRouter()

models.DataBase.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# Éstas son algo así como las consultas a la base de datos, que se alojan en la ruta que marca, no son métodos que se llamen tal cual
@router.get("/stock/{stock_id}", status_code=status.HTTP_200_OK)
async def read_uniqueStock(stock_id: int, db: db_dependency):
    stock = db.query(models.Productos).filter(
        models.Productos.id == stock_id).first()
    if stock is None:
        raise HTTPException(status_code=404, detail='Stock not Found')
    return stock

# Actualiza varios campos de un productou
class UpdateProductoModel(BaseModel):
    precio_compra: int
    precio_venta: int
    cantidad_max: int
    cantidad_min: int
    venta_max: int
    venta_min: int
@router.put("/backend/productos/{producto_id}", status_code=status.HTTP_200_OK)
async def actualizar_producto(producto_id: int, update_data: UpdateProductoModel, db: db_dependency):
    producto = db.query(models.Productos).filter(models.Productos.id == producto_id).first()
    if producto is None:
        raise HTTPException(status_code=404, detail='Producto not Found')
    producto.precio_compra = update_data.precio_compra
    producto.precio_venta = update_data.precio_venta
    producto.cantidad_max = update_data.cantidad_max
    producto.cantidad_min = update_data.cantidad_min
    producto.venta_max = update_data.venta_max
    producto.venta_min = update_data.venta_min
    db.commit()
    return {"message": f"Producto {producto_id} actualizado con éxito"}

#delete de un producto
@router.delete("/stock/{stock_id}", status_code=status.HTTP_204_NO_CONTENT)
async def borrar_producto(stock_id: int, db: db_dependency):
    stock = db.query(models.Productos).filter(
        models.Productos.id == stock_id).first()
    if stock is None:
        raise HTTPException(status_code=404, detail='Stock not Found')
    db.delete(stock)
    db.commit()
    return None  

#Para pedidos rechazados de una (cambia el status a HISTORIAL)
@router.put("/backend/pedidos/{pedido_id}/cambiar-status", status_code=status.HTTP_200_OK)
async def cambiar_status_pedido(pedido_id: int, new_status: str, db: db_dependency):
    pedido = db.query(models.Pedidos).filter(models.Pedidos.id == pedido_id).first()
    if pedido is None:
        raise HTTPException(status_code=404, detail='Pedido not Found')
    pedido.status = new_status
    db.commit()
    return {"message": f"Status del pedido {pedido_id} actualizado a {new_status}"}

#Para borrado lógico de productos
@router.put("/backend/productos/{producto_id}/cambiar-status", status_code=status.HTTP_200_OK)
async def cambiar_status_pedido(producto_id: int, new_status: int, db: db_dependency):
    producto = db.query(models.Productos).filter(models.Productos.id == producto_id).first()
    if producto is None:
        raise HTTPException(status_code=404, detail='Pedido not Found')
    producto.status = new_status
    db.commit()
    return {"message": f"Status del producto {producto_id} actualizado a {new_status}"}

# Lee la tabla de productos, pai
@router.get("/backend/stockfull", status_code=status.HTTP_200_OK)
async def read_fullStock(db: db_dependency):
    stocks = db.query(models.Productos).filter(models.Productos.status == 1).all()
    return stocks

# Este postea un pedido entrante con el formato JSON, las fechas y el id son el mismo, pero inserta múltiples registros por producto
@router.post("/backend/postPedidoEntrante", status_code=status.HTTP_201_CREATED)
async def create_pedido_entrante(request: Request, db: db_dependency):
    try:
        data = await request.json()
        total_pedido = 0  
        nuevo_pedido = models.Pedidos(
            fecha_pedido=data[0].get("fecha_pedido"),
            fecha_entrega=data[0].get("fecha_entrega"),
            metodo_pago=data[0].get("metodo_pago"),
            status='ENTRANTE',
            motivo=''
        )
        db.add(nuevo_pedido)
        db.commit()
        for producto_data in data[0]["productos"]:
            producto_id = producto_data["id"]
            cantidad = int(producto_data["cantidad"])
            producto = db.query(models.Productos).filter(models.Productos.id == producto_id).first()
            if producto:
                precio = producto.precio_venta
                total_producto = precio * cantidad
                total_pedido += total_producto
                detalle_pedido = models.Detalle_P(
                    id_pedido=nuevo_pedido.id,
                    id_producto=producto_id,
                    cantidad=cantidad,
                    precio=total_producto
                )
                db.add(detalle_pedido)
                db.commit()
        nuevo_pedido.total = total_pedido
        db.commit()
        return {"message": "Pedido entrante creado exitosamente."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# Este retorna todos los pedidos
@router.get("/backend/pedidos", status_code=status.HTTP_200_OK)
async def read_pedidosEntrantes(db: db_dependency):
    pedidos = db.query(models.Pedidos).all()
    return pedidos

# Retorna todos los pedidos ENTRANTES junto con su detalle
@router.get("/backend/pedidosEntrantes", status_code=status.HTTP_200_OK)
async def read_pedidosEntrantes(db: db_dependency):
    Pedido = aliased(models.Pedidos)
    DetallePedido = aliased(models.Detalle_P)
    Producto = aliased(models.Productos)
    query = (
        select(Pedido, DetallePedido, Producto)
        .join(DetallePedido, Pedido.id == DetallePedido.id_pedido)
        .join(Producto, DetallePedido.id_producto == Producto.id)
        .where(Pedido.status == 'ENTRANTE')
    )
    result = db.execute(query).all()
    pedidos_entrantes = []
    for row in result:
        pedido, detalle_pedido, producto = row
        pedidos_entrantes.append({
            "pedido": pedido,
            "detalle_pedido": detalle_pedido,
            "producto": producto,
        })
    return pedidos_entrantes

# Retorna todos el historial de pedidos (RECHAZADOS Y FINALIZADOS) junto con su detalle
@router.get("/backend/historialDePedidos", status_code=status.HTTP_200_OK)
async def read_pedidosEntrantes(db: db_dependency):
    Pedido = aliased(models.Pedidos)
    DetallePedido = aliased(models.Detalle_P)
    Producto = aliased(models.Productos)
    query = (
        select(Pedido, DetallePedido, Producto)
        .join(DetallePedido, Pedido.id == DetallePedido.id_pedido)
        .join(Producto, DetallePedido.id_producto == Producto.id)
        .where(Pedido.status == 'HISTORIAL')
    )
    result = db.execute(query).all()
    pedidos_entrantes = []
    for row in result:
        pedido, detalle_pedido, producto = row
        pedidos_entrantes.append({
            "pedido": pedido,
            "detalle_pedido": detalle_pedido,
            "producto": producto,
        })
    return pedidos_entrantes

# Retorna todoss los pedidos que están en curso
@router.get("/backend/pedidosEnCurso", status_code=status.HTTP_200_OK)
async def read_pedidosEntrantes(db: db_dependency):
    Pedido = aliased(models.Pedidos)
    DetallePedido = aliased(models.Detalle_P)
    Producto = aliased(models.Productos)
    query = (
        select(Pedido, DetallePedido, Producto)
        .join(DetallePedido, Pedido.id == DetallePedido.id_pedido)
        .join(Producto, DetallePedido.id_producto == Producto.id)
        .where(Pedido.status == 'EN CURSO')
    )
    result = db.execute(query).all()
    pedidos_entrantes = []
    for row in result:
        pedido, detalle_pedido, producto = row
        pedidos_entrantes.append({
            "pedido": pedido,
            "detalle_pedido": detalle_pedido,
            "producto": producto,
        })
    return pedidos_entrantes

#insert en la tabla de productos
@router.post("/backend/addproduct", status_code=status.HTTP_201_CREATED)
async def add_product(request: Request, db: db_dependency):
    try:
        data = await request.json()
        nuevo_producto = models.Productos(
            nombre=data["nombre"],
            descripcion=data["descripcion"],
            medida=data["medida"],
            precio_compra=data["precio_compra"],
            precio_venta=data["precio_venta"],
            cantidad_max=data["cantidad_max"],
            cantidad_min=data["cantidad_min"],
            status=data["status"]
        )
        db.add(nuevo_producto)
        db.commit()
        return nuevo_producto
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))