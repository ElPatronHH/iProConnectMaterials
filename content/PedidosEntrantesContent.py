from reactpy import html, component, use_state, use_effect
from database.api import getPedidosEntrantes, rechazarPedido, aceptarPedido, obtenerDetalleDePedidos, modifyStock, comprobarStockSuficiente, getItemFabricacion, addCompra  # , notificarLogistica
import asyncio
from datetime import datetime


@component
def PedidosEntrantesContent():
    pedidos, set_pedidos = use_state([])
    # motivo, set_motivo = use_state("")

    def validar_pedido_y_stock(detalle, realstock):
        stock_dict = {item['id']: item['stock'] for item in realstock}
        resultados = []
        for pedido_item in detalle:
            id_producto = pedido_item.get('id_producto')
            cantidad_pedido = pedido_item.get('cantidad')
            if id_producto is not None and cantidad_pedido is not None:
                stock_disponible = stock_dict.get(id_producto)
                if stock_disponible is not None and stock_disponible >= cantidad_pedido > 0:
                    print(
                        f"El pedido para el producto con ID {id_producto} es válido.")
                    resultados.append(True)
                else:
                    print(
                        f"El pedido para el producto con ID {id_producto} es NO válido.")
                    resultados.append(False)
            else:
                print(
                    "Error: Claves 'id_producto' o 'cantidad' no encontradas en el pedido.")
                resultados.append(False)
        return all(resultados)

    def recuperar_not_valid(detalle, realstock):
        stock_dict = {item['id']: item['stock'] for item in realstock}
        resultados = []
        for pedido_item in detalle:
            id_producto = pedido_item.get('id_producto')
            cantidad_pedido = pedido_item.get('cantidad')
            if id_producto is not None and cantidad_pedido is not None:
                stock_disponible = stock_dict.get(id_producto)
                if stock_disponible is not None and stock_disponible >= cantidad_pedido > 0:
                    print(f"xd")
                else:
                    resultados.append(
                        {"id_producto": id_producto, "cantidad": cantidad_pedido})
        print("RESULTADOS DE LOS NO VALIDOS: ", resultados)
        return resultados

    async def actualizarStock(resultados):
        for resultado in resultados:
            producto_id = resultado.get('id_producto')
            nueva_cantidad = resultado.get('nueva_cantidad')
            if producto_id is not None and nueva_cantidad is not None:
                update_data = {"stock": nueva_cantidad}
                await modifyStock(producto_id, update_data)

    def restarStock(detalle, realstock):
        stock_dict = {item['id']: item['stock'] for item in realstock}
        resultados = []
        for pedido_item in detalle:
            id_producto = pedido_item.get('id_producto')
            cantidad_pedido = pedido_item.get('cantidad')
            if id_producto is not None and cantidad_pedido is not None:
                stock_disponible = stock_dict.get(id_producto)
                if stock_disponible is not None:
                    nueva_cantidad = stock_disponible - cantidad_pedido
                    resultados.append(
                        {"id_producto": id_producto, "nueva_cantidad": nueva_cantidad})
        return resultados
    def obtener_fecha_actual():
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        return fecha_actual

    async def fillPedidos():
        pedidos_data = await getPedidosEntrantes()
        set_pedidos(pedidos_data)

    # async def handle_rechazar(pedido, motivo):
        # json = {
        # "motivo": motivo,
        # "status": "HISTORIAL"
        # }
        # await rechazarPedido(pedido, json)
        # await fillPedidos()
    # def rechazar_button_click_handler(e, pedido_id, motivo):
        # async def async_handler():
        # await handle_rechazar(pedido_id, motivo)
        # asyncio.ensure_future(async_handler())

    async def fabricacion(id_producto, cantidad, pedido_id):
        dataProducto = await getItemFabricacion(id_producto)
        print(f"La data del producto {id_producto} es esta:  ", dataProducto)
        tiempo = (dataProducto.get("tiempo_fabricacion")) * \
            (dataProducto.get("cantidad"))
        print("El tiempo de fabricación será de ", tiempo, " segundos.")
        await asyncio.sleep(10)
        # Esto se cambia hasta estar en producción para agilizar desarrollo
        # await asyncio.sleep(tiempo)
        cantidad_fabricar = cantidad - dataProducto.get("cantidad")
        nuevo_stock = dataProducto.get("cantidad") + cantidad_fabricar
        print("El total a producir es: ", cantidad_fabricar)
        new = {
            "stock": nuevo_stock
        }
        await modifyStock(id_producto, new)
        print(f"{cantidad_fabricar} de item {id_producto} agregados al inventario.")
        date = obtener_fecha_actual()
        compra_data = [{
            "id_producto": id_producto,
            "cantidad":cantidad_fabricar, 
            "fecha": date,
            "precio_total":100000
        }]
        await addCompra(compra_data)
        await handle_aceptar(pedido_id)
        
    async def handle_aceptar(pedido):
        json = {
            "status": "EN CURSO"
        }
        # Este de abajo cambia el estado a en curso del pedido, no desactivar hasta que esté ready el desarrollo
        await aceptarPedido(pedido, json)
        await fillPedidos()

    def aceptar_button_click_handler(e, pedido_id):
        async def async_handler():
            detalle = await obtenerDetalleDePedidos(pedido_id)
            if detalle:
                print("Detalle: ", detalle)
                id_productoList = []
                for detalle_item in detalle:
                    id_producto = int(detalle_item["id_producto"])
                    id_productoList.append(id_producto)
                realstock = await comprobarStockSuficiente(id_productoList)
                if realstock:
                    print("Real Stock: ", realstock)
                    if validar_pedido_y_stock(detalle, realstock):
                        # Aquí ya se sabe que es un pedido que podemos cumplir sin problemas, toda notificar a Logística y ver si ellos pueden rechazar o sí o sí responden y restamos de una el inventario
                        newStock = restarStock(detalle, realstock)
                        print("New Stock: ", newStock)
                        await actualizarStock(newStock)
                        await handle_aceptar(pedido_id)
                    else:
                        print("Stock insuficiente, se requiere producir.")
                        productos_a_fabricar = recuperar_not_valid(
                            detalle, realstock)
                        for producto in productos_a_fabricar:
                            await fabricacion(producto.get('id_producto'), producto.get('cantidad'), pedido_id)
        asyncio.ensure_future(async_handler())

    use_effect(fillPedidos)

    def render_detalle_pedido(pedido_item):
        return html.div({"key": pedido_item["detalle_pedido"]["id"],
                        "class": "card card-body mb-2"},
                        html.div({"class": "card-body"},
                        html.div({"class": "card-title"},
                                 f"Producto: {pedido_item['producto']['nombre']}"),
                        html.p(
                            f"Cantidad: {pedido_item['detalle_pedido']['cantidad']}")
        )
        )

    grouped_pedidos = {}
    for pedido_item in pedidos:
        pedido_id = pedido_item["pedido"]["id"]
        if pedido_id not in grouped_pedidos:
            grouped_pedidos[pedido_id] = []
        grouped_pedidos[pedido_id].append(pedido_item)
    cards = []

    for pedido_id, grupo_pedidos in grouped_pedidos.items():
        cards.append(html.div({"class": "grupo-tarjeta"},
                              html.h5({"class": "card-title"},
                                      f"PEDIDO {pedido_id}",
                                      html.p(
                                  f"Fecha: {pedido_item['pedido']['fecha_entrega']}"),
            html.div({"class": "botonera-card"},
                                  html.button({"class": "btn btn-primary",
                                               # lambda e, pedido_id=pedido_id: aceptar_button_click_handler(e, pedido_id, id_productos)
                                               "onclick": lambda e, pedido_id=pedido_id: aceptar_button_click_handler(e, pedido_id)
                                               },
                                              "Aceptar"
                                              ),
                                  # html.button({"class": "btn btn-danger",
                                  # "onclick": lambda e, pedido_id=pedido_id: rechazar_button_click_handler(e, pedido_id, motivo)
                                  # },
                                  # "Rechazar"
                                  # )
                     )),
            # html.div({"class": "input-centrado"},
            #         html.input(
            #    {
            #        "type": "text",
            #       "placeholder": "Motivo en caso de rechazo...",
            #        "onChange": lambda e: set_motivo(e["target"]["value"])
            #    }
            # )),
            [render_detalle_pedido(pedido_item)
             for pedido_item in grupo_pedidos]
        )
        )
    return html.div(
        html.h2({"class": "titulo-pantalla"}, "PEDIDOS ENTRANTES"),
        html.div({"class": "pedidos-container"}, cards)
    )
