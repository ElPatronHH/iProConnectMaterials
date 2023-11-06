--2.0
-- Tabla Productos
CREATE TABLE productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255),
    descripcion VARCHAR(255),
    medida VARCHAR(50),
    precio_compra DECIMAL(10, 2),
    precio_venta DECIMAL(10, 2),
    cantidad_max INT,
    cantidad_min INT,
    status VARCHAR(20)
);

-- Tabla Compras
CREATE TABLE compras (
    id INT AUTO_INCREMENT PRIMARY KEY,
    producto_id INT,
    cantidad INT,
    productos_precio_compra DECIMAL(10, 2),
    productos_medida VARCHAR(50),
    fecha DATE,
    precio_total DECIMAL(10, 2),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);

-- Tabla Pedidos
CREATE TABLE pedidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    producto_id INT,
    cantidad_total INT,
    status VARCHAR(20),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);

-- Tabla Ventas
CREATE TABLE ventas (
    venta_id INT AUTO_INCREMENT PRIMARY KEY,
    pedido_id INT,
    pedidos_cantidad_total INT,
    pedidos_metodo_pago VARCHAR(50),
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id)
);

-- Tabla Pedidos Entrantes
CREATE TABLE pedidoentrante (
    id INT AUTO_INCREMENT PRIMARY KEY,  
    pedido_id INT,
    producto_id INT,                    
    fecha_pedido DATE,                  
    fecha_entrega DATE,                 
    cantidad INT,                                   
    metodo_pago VARCHAR(50),           
    FOREIGN KEY (producto_id) REFERENCES productos(id),
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id)
);

-- Tabla Logistica
CREATE TABLE logistica (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pedido_id INT,
    fecha_embarque DATE,
    fecha_embarqueRecibido DATE,
    metodoPago VARCHAR(50),
    precio DECIMAL(10, 2),
    status VARCHAR(20),
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id)
);


--Datos de Prueba
INSERT INTO productos (nombre, descripcion, medida, precio_compra, precio_venta, cantidad_max, cantidad_min, status)
VALUES ('T3_B_0COB0', 'Cobre', 'Unidad', 10.00, 20.00, 100, 10, 'Disponible');

INSERT INTO productos (nombre, descripcion, medida, precio_compra, precio_venta, cantidad_max, cantidad_min, status)
VALUES ('T3_B_0ALU1', 'Aluminio', 'Unidad', 15.00, 25.00, 150, 20, 'Disponible');

INSERT INTO productos (nombre, descripcion, medida, precio_compra, precio_venta, cantidad_max, cantidad_min, status)
VALUES ('T3_B_0SIL2', 'Silicio', 'Kilogramo', 5.00, 10.00, 50, 5, 'Disponible');

INSERT INTO productos (nombre, descripcion, medida, precio_compra, precio_venta, cantidad_max, cantidad_min, status)
VALUES ('T3_B_0ORO3', 'Oro', 'Kilogramo', 5.00, 10.00, 50, 5, 'Disponible');

INSERT INTO productos (nombre, descripcion, medida, precio_compra, precio_venta, cantidad_max, cantidad_min, status)
VALUES ('T3_B_0EST4', 'Estaño', 'Kilogramo', 5.00, 10.00, 50, 5, 'Disponible');

INSERT INTO productos (nombre, descripcion, medida, precio_compra, precio_venta, cantidad_max, cantidad_min, status)
VALUES ('T3_B_0PLA5', 'Plata', 'Kilogramo', 5.00, 10.00, 50, 5, 'Disponible');

INSERT INTO productos (nombre, descripcion, medida, precio_compra, precio_venta, cantidad_max, cantidad_min, status)
VALUES ('T3_B_0VID6', 'Vidrio', 'Kilogramo', 5.00, 10.00, 50, 5, 'Disponible');

INSERT INTO productos (nombre, descripcion, medida, precio_compra, precio_venta, cantidad_max, cantidad_min, status)
VALUES ('T3_B_0LIT7', 'Litio', 'Kilogramo', 5.00, 10.00, 50, 5, 'Disponible');


INSERT INTO compras (producto_id, cantidad, productos_precio_compra, productos_medida, fecha, precio_total)
VALUES (1, 50, 10.00, 'Unidad', '2023-11-05', 500.00);

INSERT INTO pedidos (producto_id, cantidad_total, status)
VALUES (default, 20, 'En espera');
INSERT INTO pedidos (producto_id, cantidad_total, status)
VALUES (default, 20, 'En espera');
INSERT INTO pedidos (producto_id, cantidad_total, status)
VALUES (default, 20, 'En espera');
INSERT INTO ventas (pedido_id, pedidos_cantidad_total, pedidos_metodo_pago)
VALUES (1, 20, 'Tarjeta de crédito');

INSERT INTO pedidoentrante (pedido_id, producto_id, fecha_pedido, fecha_entrega, cantidad, metodo_pago)
VALUES (default, 1, '2023-11-05', '2023-11-15', 30, 'Efectivo');
INSERT INTO pedidoentrante (pedido_id, producto_id, fecha_pedido, fecha_entrega, cantidad, metodo_pago)
VALUES (default, 2, '2023-11-05', '2023-11-15', 30, 'Efectivo');
INSERT INTO pedidoentrante (pedido_id, producto_id, fecha_pedido, fecha_entrega, cantidad, metodo_pago)
VALUES (default, 3, '2023-11-05', '2023-11-15', 30, 'Efectivo');

--T3_B_00000 (Tier 3 Proveedor pantallas )
--3.0 Explicación, no importa
-- Tabla Pedidos
CREATE TABLE pedidoentrante (
    id INT AUTO_INCREMENT PRIMARY KEY,  --auto, pero debe coincidir si se mandan varios productos en un solo pedido
    producto_id INT,                    --aquí el producto solicitado
    fecha_pedido DATE,                  --fecha actual en que se solicita
    fecha_entrega DATE,                 --fecha en la que se pide
    cantidad INT,                       --cuantos del material              
    metodo_pago VARCHAR(50),            --formato de pago
    FOREIGN KEY (producto_id) REFERENCES Productos(id)
);

--EJEMPLO DE SOLICITUD POST PARA PEDIDO
[
  {
    "pedido_id":1, --Aquí para aclarar que todo es parte del mismo pedido.
    "id":1, --Este, ¿Cómo ves?, creo que puede ser un auto increment en nuestro sistema, entonces quizá no lo tengas que proporcionar.
    "productos":[
      {
        "id":1, --Te voy a pasar los id de nuestro "catálogo"
        "cantidad":"200" --Cuántos de ese material
      },
      {
        "id":2, --Te voy a pasar los id de nuestro "catálogo"
        "cantidad":"300" --Cuántos de ese material
      }
    ],
    "fecha_pedido":"2023-01-10", -- Esta que sea la fecha del día que se manda, la recuperas en tu código plx
    "fecha_entrega":"2023-01-10", -- Para cuando ocupas el material
    "metodo_pago":"Tarjeta" --Tarjeta o no sé, eso lo dijo el profe, queda pendiente preguntar los tipos de pago aceptados xd
  }
]

[
  {
    "pedido_id":1, 
    "productos":[
      {
        "id":1, 
        "cantidad":"200" 
      },
      {
        "id":2, 
        "cantidad":"300" 
      }
    ],
    "fecha_pedido":"2023-01-10",
    "fecha_entrega":"2023-01-10", 
    "metodo_pago":"Tarjeta"
  }
]

http://127.0.0.1:8000/backend/pedidoEntrante