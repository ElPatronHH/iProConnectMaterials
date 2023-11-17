from sqlalchemy import Column, Integer, String, DECIMAL, Date, Enum, ForeignKey
from database.database import DataBase

class Productos(DataBase):
    __tablename__ = 'productos'
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nombre = Column(String(20))
    descripcion = Column(String(20))
    medida = Column(String(20))
    precio_compra = Column(Integer)
    precio_venta = Column(Integer)
    stock = Column(Integer)
    cantidad_max = Column(Integer)
    cantidad_min = Column(Integer)
    venta_max = Column(Integer)
    venta_min = Column(Integer)
    tiempo_fabricacion = Column(Integer)
    status = Column(Integer)

class Pedidos(DataBase):
    __tablename__ = 'pedidos'
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    fecha_pedido = Column(Date)
    fecha_entrega = Column(Date)
    metodo_pago = Column(String(20))
    total = Column(Integer)
    status = Column(Enum('ENTRANTE', 'EN CURSO', 'HISTORIAL'))
    motivo = Column(String(200))
    
class Detalle_P (DataBase):
    __tablename__ = 'detalle_p'
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    id_pedido = Column(Integer, ForeignKey('pedidos.id'))
    id_producto = Column(Integer, ForeignKey('productos.id'))
    precio = Column(Integer)
    cantidad = Column(Integer)
    
    
class Compras(DataBase):
    __tablename__ = 'compras'
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    id_producto = Column(Integer, ForeignKey('productos.id'))
    cantidad = Column(Integer)
    fecha = Column(Date)
    precio_total = Column(Integer)
    
"""
class Logistica(DataBase):
    __tablename__ = 'logistica'
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    pedido_id = Column(Integer, ForeignKey('pedidos.id'))
    fecha_embarque = Column(Date)
    fecha_embarqueRecibido = Column(Date)
    metodoPago = Column(String(50))
    precio = Column(DECIMAL(10, 2))
    status = Column(String(20))

class Ventas(DataBase):
    __tablename__ = 'ventas'
    
    venta_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    pedido_id = Column(Integer, ForeignKey('pedidos.id'))
    pedidos_cantidad_total = Column(Integer)
    pedidos_metodo_pago = Column(String(50))"""