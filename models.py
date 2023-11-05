from sqlalchemy import Column, Integer, String, DECIMAL, Date, ForeignKey
from database.database import DataBase

class Productos(DataBase):
    __tablename__ = 'productos'
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nombre = Column(String(255))
    descripcion = Column(String(255))
    medida = Column(String(50))
    precio_compra = Column(DECIMAL(10, 2))
    precio_venta = Column(DECIMAL(10, 2))
    cantidad_max = Column(Integer)
    cantidad_min = Column(Integer)
    status = Column(String(20))

class Compras(DataBase):
    __tablename__ = 'compras'
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    producto_id = Column(Integer, ForeignKey('productos.id'))
    cantidad = Column(Integer)
    productos_precio_compra = Column(DECIMAL(10, 2))
    productos_medida = Column(String(50))
    fecha = Column(Date)
    precio_total = Column(DECIMAL(10, 2))

class Pedidos(DataBase):
    __tablename__ = 'pedidos'
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    producto_id = Column(Integer, ForeignKey('productos.id'))
    fecha_pedido = Column(Date)
    fecha_entrega = Column(Date)
    cantidad = Column(Integer)
    cantidad_total = Column(Integer)
    metodo_pago = Column(String(50))
    status = Column(String(20))
    
class PedidoEntrante(DataBase):
    __tablename__ = 'pedidoentrante'
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    producto_id = Column(Integer, ForeignKey('productos.id'))
    fecha_pedido = Column(Date)
    fecha_entrega = Column(Date)
    cantidad = Column(Integer)
    metodo_pago = Column(String(50))

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
    pedidos_metodo_pago = Column(String(50))
