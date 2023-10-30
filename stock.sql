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
