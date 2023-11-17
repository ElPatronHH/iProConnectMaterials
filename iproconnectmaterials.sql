-- 3.0
CREATE TABLE productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(20),
    descripcion VARCHAR(20),
    medida VARCHAR(20),
    precio_compra INT,
    precio_venta INT,
    stock INT,
    cantidad_max INT,
    cantidad_min INT,
    venta_max INT,
    venta_min INT,
    tiempo_fabricacion INT,
    status INT
);

CREATE TABLE pedidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha_pedido DATE,
    fecha_entrega DATE,
    metodo_pago VARCHAR(20),
    total INT,
    status ENUM('ENTRANTE', 'EN CURSO', 'HISTORIAL'),
    motivo VARCHAR(200)
);

CREATE TABLE detalle_p (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_pedido INT,
    id_producto INT,
    cantidad INT,
    precio INT,
    FOREIGN KEY (id_pedido) REFERENCES pedidos(id),
    FOREIGN KEY (id_producto) REFERENCES productos(id)
);

CREATE TABLE compras (
   id INT AUTO_INCREMENT PRIMARY KEY,
   id_producto INT,
   cantidad INT,
   fecha DATE,
   precio_total INT,
   FOREIGN KEY (id_producto) REFERENCES productos(id)
);

-- Datos de prueba para la tabla productos
-- 1, precio: 20
INSERT INTO productos (nombre, descripcion, medida, precio_compra, precio_venta, stock, cantidad_max, cantidad_min, venta_max, venta_min, tiempo_fabricacion, status)
VALUES ('T3_B_0COB1', 'Cobre', 'Unidad', 10, 20,2000, 100, 10, 1000, 1, 2, 1);
-- 2, precio: 25
INSERT INTO productos (nombre, descripcion, medida, precio_compra, precio_venta, stock, cantidad_max, cantidad_min, venta_max, venta_min, tiempo_fabricacion,status)
VALUES ('T3_B_0ALU2', 'Aluminio', 'Unidad', 15, 25,2000, 150, 20, 1000, 1, 2, 1);
-- 3, precio: 10
INSERT INTO productos (nombre, descripcion, medida, precio_compra, precio_venta, stock, cantidad_max, cantidad_min, venta_max, venta_min, tiempo_fabricacion,status)
VALUES ('T3_B_0SIL3', 'Silicio', 'Kilogramo', 5, 10,2000, 50, 5, 1000, 1, 2, 1);
-- 4, precio: 10
INSERT INTO productos (nombre, descripcion, medida, precio_compra, precio_venta, stock, cantidad_max, cantidad_min, venta_max, venta_min, tiempo_fabricacion,status)
VALUES ('T3_B_0ORO4', 'Oro', 'Kilogramo', 5, 10,2000, 50, 5, 1000, 1, 2, 1);
-- 5, precio: 10
INSERT INTO productos (nombre, descripcion, medida, precio_compra, precio_venta, stock, cantidad_max, cantidad_min, venta_max, venta_min, tiempo_fabricacion,status)
VALUES ('T3_B_0EST5', 'Estaño', 'Kilogramo', 5, 10,2000, 50, 5, 1000, 1, 2, 1);
-- 6, precio: 10
INSERT INTO productos (nombre, descripcion, medida, precio_compra, precio_venta, stock, cantidad_max, cantidad_min, venta_max, venta_min, tiempo_fabricacion,status)
VALUES ('T3_B_0PLA6', 'Plata', 'Kilogramo', 5, 10,2000, 50, 5, 1000, 1, 2, 1);
-- 7, precio: 10
INSERT INTO productos (nombre, descripcion, medida, precio_compra, precio_venta, stock, cantidad_max, cantidad_min, venta_max, venta_min, tiempo_fabricacion,status)
VALUES ('T3_B_0VID7', 'Vidrio', 'Kilogramo', 5, 10,2000, 50, 5, 1000, 1, 2, 1);
-- 8, precio: 10
INSERT INTO productos (nombre, descripcion, medida, precio_compra, precio_venta, stock, cantidad_max, cantidad_min, venta_max, venta_min, tiempo_fabricacion,status)
VALUES ('T3_B_0LIT8', 'Litio', 'Kilogramo', 5, 10,2000, 50, 5, 1000, 1, 2, 1);

-- Datos de prueba para la tabla pedidos
INSERT INTO pedidos (fecha_pedido, fecha_entrega, metodo_pago, total, status, motivo) VALUES
('2023-11-06', '2023-11-10', 'Tarjeta de crédito', 325, 'EN CURSO', ''),
('2023-11-07', '2023-11-12', 'Efectivo', 325, 'ENTRANTE', ''),
('2023-11-08', '2023-11-14', 'Transferencia bancaria', 1600, 'ENTRANTE', '');
-- Datos de prueba para la tabla detalle_p (Detalles de los pedidos)
INSERT INTO detalle_p (id_pedido, id_producto, cantidad, precio) VALUES
(1, 1, 10, 200),
(1, 2, 5, 125);
INSERT INTO detalle_p (id_pedido, id_producto, cantidad, precio) VALUES
(2, 2, 5, 125),
(2, 3, 20, 200);
INSERT INTO detalle_p (id_pedido, id_producto, cantidad, precio) VALUES
(3, 1, 70, 1400),
(3, 3, 20, 200);
-- Datos de prueba para la tabla compras
INSERT INTO compras (id_producto, cantidad, fecha, precio_total) VALUES
(1, 100, '2023-11-01', 2000),
(2, 50, '2023-11-02', 1250),
(3, 30, '2023-11-03', 300);


--EJEMPLO DE SOLICITUD POST PARA PEDIDO
[
  {
    "productos":[
      {
        "id":1, --Te voy a pasar los id de nuestro "catálogo"
        "cantidad":"2" --Cuántos de ese material
      },
      {
        "id":2, --Te voy a pasar los id de nuestro "catálogo"
        "cantidad":"3" --Cuántos de ese material
      }
    ],
    "fecha_pedido":"2023-01-10", -- Esta que sea la fecha del día que se manda, la recuperas en tu código plx
    "fecha_entrega":"2023-01-10", -- Para cuando ocupas el material
    "metodo_pago":"Tarjeta" --Tarjeta o no sé, eso lo dijo el profe, queda pendiente preguntar los tipos de pago aceptados xd
  }
]

[
  {
    "productos":[
      {
        "id":1, 
        "cantidad":"2" 
      },
      {
        "id":2, 
        "cantidad":"3" 
      }
    ],
    "fecha_pedido":"2023-01-10",
    "fecha_entrega":"2023-01-10", 
    "metodo_pago":"Tarjeta"
  }
]

http://127.0.0.1:8000/backend/postPedidoEntrante









































--INVENTARIOS CONTENT INPUT
from reactpy import html, component, use_state, use_effect, use_ref
from database.api import getStock, deleteProducto, addProducto
import asyncio

@component
def InventariosContent():
    stock, set_stock = use_state([])
    nombre_input, set_nombre_input = use_state('')
    descripcion_input, set_descripcion_input = use_state('')
    medida_input, set_medida_input = use_state('')
    precio_compra_input, set_precio_compra_input = use_state(0)
    precio_venta_input, set_precio_venta_input = use_state(0)
    cantidad_max_input, set_cantidad_max_input = use_state(0)
    cantidad_min_input, set_cantidad_min_input = use_state(0)
    status_input, set_status_input = use_state('')

    async def fillItems():
        stock_data = await getStock()
        set_stock(stock_data)

    async def handle_delete(producto):
        await deleteProducto(producto)
        await fillItems()

    async def handle_add_product():
        new_product = {
            "nombre": nombre_input,
            "descripcion": descripcion_input,
            "medida": medida_input,
            "precio_compra": precio_compra_input,
            "precio_venta": precio_venta_input,
            "cantidad_max": cantidad_max_input,
            "cantidad_min": cantidad_min_input,
            "status": status_input,
        }
        await addProducto(new_product)
        await fillItems()
        set_nombre_input('')
        set_descripcion_input('')
        set_medida_input('')
        set_precio_compra_input(0)
        set_precio_venta_input(0)
        set_cantidad_max_input(0)
        set_cantidad_min_input(0)
        set_status_input('')

    def delete_button_click_handler(e, producto_id):
        async def async_handler():
            await handle_delete(producto_id)
        asyncio.ensure_future(async_handler())

    def render_stock_item(stock_item):
        return html.div(
            {
                "key": stock_item["id"],
                "class": "card card-body mb-2"
            },
            html.p({"class": "card-title"}, stock_item["nombre"]),
            html.p({"class": "centered-p"}, f"{stock_item['descripcion']}"),
            html.p(f"ID: {stock_item['id']}"),
             html.p(f"Medida: {stock_item['medida']}"),
            html.p(f"Precio de compra: {stock_item['precio_compra']}"),
            html.p(f"Precio de venta: {stock_item['precio_venta']}"),
             html.p(f"Cantidad Máxima: {stock_item['cantidad_max']}"),
              html.p(f"Cantidad Mínima: {stock_item['cantidad_min']}"),
               html.p(f"Status: {stock_item['status']}"),
            html.div({"class": "botonera-card"},
                     html.button({"class": "btn",
                                   #"onclick": lambda event: delete_product(stock_item["id"])
                                  },
                                 "Modificar"
                                 ),
                     html.button({"class": "btn btn-danger",
                                  "onclick": lambda e: delete_button_click_handler(e, stock_item["id"])
                                  },
                                 "Eliminar"
                                 )
                     )
        )


    return html.div(
        html.h2({"class": "titulo-pantalla"}, "INVENTARIO"),
        html.div({"class": "pedidos-container"}, [
            html.div({"class": "cardv2"}, [
                html.button({"class": "btn btn-primary", "onclick": handle_add_product}, "Añadir Producto"),
                html.form({"onSubmit": handle_add_product}, [
                    html.label("Nombre:"),
                    html.input({"type": "text", "value": nombre_input, "onChange": lambda e: set_nombre_input(e.target.value)}),
                    html.label("Descripción:"),
                    html.input({"type": "text", "value": descripcion_input, "onChange": lambda e: set_descripcion_input(e.target.value)}),
                    html.label("Medida:"),
                    html.input({"type": "text", "value": medida_input, "onChange": lambda e: set_medida_input(e.target.value)}),
                    html.label("Precio de Compra:"),
                    html.input({"type": "number", "value": precio_compra_input, "onChange": lambda e: set_precio_compra_input(float(e.target.value))}),
                    html.label("Precio de Venta:"),
                    html.input({"type": "number", "value": precio_venta_input, "onChange": lambda e: set_precio_venta_input(float(e.target.value))}),
                    html.label("Cantidad Máxima:"),
                    html.input({"type": "number", "value": cantidad_max_input, "onChange": lambda e: set_cantidad_max_input(int(e.target.value))}),
                    html.label("Cantidad Mínima:"),
                    html.input({"type": "number", "value": cantidad_min_input, "onChange": lambda e: set_cantidad_min_input(int(e.target.value))}),
                    html.label("Status:"),
                    html.input({"type": "text", "value": status_input, "onChange": lambda e: set_status_input(e.target.value)}),
                    html.button({"type": "submit"}, "Agregar Producto")
                ]),
            ])
        ]),
        [render_stock_item(stock_item) for stock_item in stock]
    )
