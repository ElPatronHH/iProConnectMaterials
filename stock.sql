SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

CREATE TABLE `stock` (
  `id` int(255) NOT NULL,
  `descripcion` varchar(255) NOT NULL,
  `numParte` int(255) NOT NULL,
  `curentStock` int(255) NOT NULL,
  `maxVenta` int(255) NOT NULL,
  `minVenta` int(255) NOT NULL,
  `puntoMax` int(255) NOT NULL,
  `puntoReorden` int(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

ALTER TABLE `stock`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `stock`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT;
COMMIT;

--T3_B_0000P (Tier 3 - Pantallas) 
--T3_B_0000B (Tier 3 - Bocinas)
--T3_B_0000C (Tier 3 - Cables)
--id, nombre pieza, cantidad, mínimo de venta, máximo de venta, punto de reorden, stock máximo
INSERT INTO `stock`(`id`, `descripcion`, `numParte`, `currentStock`, `maxVenta`, `minVenta`, `puntoMax`, `puntoReorden`) VALUES ('','Pantallas','T3_B_0000P','50','10','50','20','500');
INSERT INTO `stock`(`id`, `descripcion`, `numParte`, `currentStock`, `maxVenta`, `minVenta`, `puntoMax`, `puntoReorden`) VALUES ('','Bocinas','T3_B_0000B','50','10','50','20','500');
INSERT INTO `stock`(`id`, `descripcion`, `numParte`, `currentStock`, `maxVenta`, `minVenta`, `puntoMax`, `puntoReorden`) VALUES ('','Cables','T3_B_0000C','50','10','50','20','500');


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
    FOREIGN KEY (producto_id) REFERENCES Productos(id)
);

-- Tabla Pedidos
CREATE TABLE pedidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    producto_id INT,
    fecha_pedido DATE,
    fecha_entrega DATE,
    cantidad INT,
    cantidad_total INT,
    metodo_pago VARCHAR(50),
    status VARCHAR(20),
    FOREIGN KEY (producto_id) REFERENCES Productos(id)
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
    FOREIGN KEY (pedido_id) REFERENCES Pedidos(id)
);

-- Tabla Ventas
CREATE TABLE ventas (
    venta_id INT AUTO_INCREMENT PRIMARY KEY,
    pedido_id INT,
    pedidos_cantidad_total INT,
    pedidos_metodo_pago VARCHAR(50),
    FOREIGN KEY (pedido_id) REFERENCES Pedidos(id)
);



--3.0
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

[
  {
    "id":1, --Este, ¿Cómo ves?, creo que puede ser un auto increment en nuestro sistema, entonces quizá no lo tengas que proporcionar.
    "productos":[
      {
        "id":1, --Te voy a pasar los id de nuestro "catálogo"
        "cantidad":"200", --Cuántos de ese material
      },
      {
        "id":2, --Te voy a pasar los id de nuestro "catálogo"
        "cantidad":"300", --Cuántos de ese material
      }
    ],
    "fecha_pedido":"2023-01-10", -- Esta que sea la fecha del día que se manda, la recuperas en tu código plx
    "fecha_entrega":"2023-01-10", -- Para cuando ocupas el material
    "metodo_pago":"Tarjeta" --Tarjeta o no sé, eso lo dijo el profe, queda pendiente preguntar los tipos de pago aceptados xd
  }
]