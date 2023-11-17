from fastapi import APIRouter, HTTPException, Depends, status, Request, Path
from typing import Annotated
from typing import List
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

# Éstas son algo así como las consultas a la base de datos, que se alojan en la ruta que marca, no son métodos que se llamen tal cual, aquí el primero es para obtener data de un solo producto, no sirve pa nada pq no lo usamos, pero parar probar
@router.get("/stock/{stock_id}", status_code=status.HTTP_200_OK)
async def read_unique_stock(stock_id: int, db: db_dependency):
    stock = db.query(models.Productos).filter(
        models.Productos.id == stock_id).first()
    if stock is None:
        raise HTTPException(status_code=404, detail='Stock not Found')
    return stock

# Actualiza varios campos de un productou, ocupamos model
class UpdateProductoModel(BaseModel):
    nombre: str
    descripcion: str
    medida: str
    stock: int
    precio_compra: int
    precio_venta: int
    cantidad_max: int
    cantidad_min: int
    venta_max: int
    venta_min: int
@router.put("/backend/productos/{producto_id}", status_code=status.HTTP_200_OK)
async def update_product(producto_id: int, update_data: UpdateProductoModel, db: db_dependency):
    producto = db.query(models.Productos).filter(
        models.Productos.id == producto_id).first()
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

# Delete real de un producto
@router.delete("/stock/{stock_id}", status_code=status.HTTP_204_NO_CONTENT)
async def borrar_permanentemente_product(stock_id: int, db: db_dependency):
    stock = db.query(models.Productos).filter(
        models.Productos.id == stock_id).first()
    if stock is None:
        raise HTTPException(status_code=404, detail='Stock not Found')
    db.delete(stock)
    db.commit()
    return None

# Para borrado lógico de productos
@router.put("/backend/productos/{producto_id}/cambiar-status", status_code=status.HTTP_200_OK)
async def borrar_logicamente_product(producto_id: int, new_status: int, db: db_dependency):
    producto = db.query(models.Productos).filter(
        models.Productos.id == producto_id).first()
    if producto is None:
        raise HTTPException(status_code=404, detail='Pedido not Found')
    producto.status = new_status
    db.commit()
    return {"message": f"Status del producto {producto_id} actualizado a {new_status}"}

# Lee la tabla de productos con un 1 en status, pai
@router.get("/backend/stockfull", status_code=status.HTTP_200_OK)
async def read_full_stock(db: db_dependency):
    stocks = db.query(models.Productos).filter(
        models.Productos.status == 1).all()
    return stocks

# Este postea un pedido entrante con el formato JSON, las fechas y el id son el mismo, pero inserta múltiples registros por producto
@router.post("/backend/postPedidoEntrante", status_code=status.HTTP_201_CREATED)
async def add_pedido_entrante(request: Request, db: db_dependency):
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
            producto = db.query(models.Productos).filter(
                models.Productos.id == producto_id).first()
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
async def read_todos_pedidos(db: db_dependency):
    pedidos = db.query(models.Pedidos).all()
    return pedidos

# Retorna todos los pedidos ENTRANTES junto con su detalle
@router.get("/backend/pedidosEntrantes", status_code=status.HTTP_200_OK)
async def read_pedidos_entrantes(db: db_dependency):
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
async def read_pedidos_en_historial(db: db_dependency):
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
async def read_pedidos_en_curso(db: db_dependency):
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

# insert en la tabla de productos
@router.post("/backend/addproduct", status_code=status.HTTP_201_CREATED)
async def add_product(request: Request, db: db_dependency):
    try:
        data = await request.json()
        if isinstance(data, list) and len(data) > 0:
            product_data = data[0]
            nuevo_producto = models.Productos(
                nombre=product_data["nombre"],
                descripcion=product_data["descripcion"],
                medida=product_data["medida"],
                stock=product_data["stock"],
                precio_compra=product_data["precio_compra"],
                precio_venta=product_data["precio_venta"],
                cantidad_max=product_data["cantidad_max"],
                cantidad_min=product_data["cantidad_min"],
                venta_max=product_data["venta_max"],
                venta_min=product_data["venta_min"],
                status=product_data["status"]
            )
            db.add(nuevo_producto)
            db.commit()
            return nuevo_producto
        else:
            raise HTTPException(status_code=400, detail="Invalid JSON format")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# Para pedidos rechazados de una (cambia el status a HISTORIAL)
class UpdatePedidoModel(BaseModel):
    motivo: str
    status: str
@router.put("/backend/pedidos/{pedido_id}", status_code=status.HTTP_200_OK)
async def rechazar_pedido_con_motivo(pedido_id: int, update_data: UpdatePedidoModel, db: db_dependency):
    pedido = db.query(models.Pedidos).filter(
        models.Pedidos.id == pedido_id).first()
    if pedido is None:
        raise HTTPException(status_code=404, detail='Pedido not Found')
    pedido.motivo = update_data.motivo
    pedido.status = update_data.status
    db.commit()
    return {"message": f"Pedido {pedido_id} rechazado con éxito y se agregó el motivo: {pedido.motivo}."}

#Para aceptar un pedido y pasarlo a pedido entrante
class AcceptPedidoModel(BaseModel):
    status: str
@router.put("/backend/acceptpedido/{pedido_id}", status_code=status.HTTP_200_OK)
async def aceptar_pedido(pedido_id: int, update_data: AcceptPedidoModel, db: db_dependency):
    pedido = db.query(models.Pedidos).filter(
        models.Pedidos.id == pedido_id).first()
    if pedido is None:
        raise HTTPException(status_code=404, detail='Pedido not Found')
    pedido.status = update_data.status
    db.commit()
    return {"message": f"Pedido {pedido_id} aceptado con éxito."}

#Para solicitar datos relevantes previos a la aceptación (Productos:	id, stock, tiempo_fabricacion)
@router.post("/backend/comprobacion_stock", status_code=status.HTTP_200_OK)
async def comprobacion_stock(product_ids: List[int], db: Session = Depends(get_db)):
    productos = db.query(models.Productos).filter(
        models.Productos.id.in_(product_ids),
        models.Productos.status == 1
    ).all()
    if len(productos) != len(set(product_ids)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Al menos un producto no encontrado")
    response_data = [{"id": producto.id, "stock": producto.stock} for producto in productos]
    return response_data

# Obtener detalles de pedidos para un pedido específico
@router.get("/backend/detalle_pedidos", status_code=status.HTTP_200_OK)
async def read_detalle_pedidos(db: db_dependency, pedido_id: int):
    Pedido = aliased(models.Pedidos)
    DetallePedido = aliased(models.Detalle_P)
    query = (
        select(DetallePedido.id_producto, DetallePedido.cantidad)
        .join(Pedido, Pedido.id == DetallePedido.id_pedido) 
        .where(Pedido.id == pedido_id)
    )
    result = db.execute(query).all()
    detalles_pedidos = []
    for row in result:
        id_producto, cantidad = row
        detalles_pedidos.append({
            "id_producto": id_producto,
            "cantidad": cantidad,
        })
    return detalles_pedidos

# Actualiza el stock después de una venta
class UpdateStockModel(BaseModel):
    stock: int
@router.put("/backend/productos_new_stock/{producto_id}", status_code=status.HTTP_200_OK)
async def update_stock_product(producto_id: int, update_data: UpdateStockModel, db: db_dependency):
    producto = db.query(models.Productos).filter(
        models.Productos.id == producto_id).first()
    if producto is None:
        raise HTTPException(status_code=404, detail='Producto not Found')
    a = producto.stock
    producto.stock = update_data.stock
    db.commit()
    return {"message": f"Producto {producto_id} actualizado de {a} a {update_data.stock}."}

# Lee la tabla de productos y retorna del que le des id
@router.get("/backend/producto_tiempo/{producto_id}", status_code=status.HTTP_200_OK)
async def read_tiempo_cantidad(db: db_dependency, producto_id: int):
    product = db.query(models.Productos).filter(
        models.Productos.id == producto_id).first()
    if product:
        return {"tiempo_fabricacion": product.tiempo_fabricacion, "cantidad": product.stock}
    else:
        return {"error": "Producto no encontrado"}