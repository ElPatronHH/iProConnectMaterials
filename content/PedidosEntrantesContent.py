from reactpy import html, component, use_state, use_effect
from database.api import getPedidosEntrantes, rechazarPedido, aceptarPedido, obtenerDetalleDePedidos, modifyStock, comprobarStockSuficiente#, notificarLogistica
import asyncio
@component
def PedidosEntrantesContent():
    pedidos, set_pedidos = use_state([])
    motivo, set_motivo = use_state("")

    def validar_pedido_y_stock(detalle, realstock):
        todocool = True
        stock_dict = {item['id']: item['stock'] for item in realstock}
        for pedido_item in detalle:
            id_producto = pedido_item.get('id_producto')
            cantidad_pedido = pedido_item.get('cantidad')
            if id_producto is not None and cantidad_pedido is not None:
                stock_disponible = stock_dict.get(id_producto)
                if stock_disponible is not None and stock_disponible >= cantidad_pedido > 0:
                    print(f"El pedido para el producto con ID {id_producto} es válido.")
                    return todocool
                else:
                    print(f"Error: No hay suficiente stock para el producto con ID {id_producto}.")
                    return not todocool
            else:
                print("Error: Claves 'id_producto' o 'cantidad' no encontradas en el pedido.")
                return not todocool
            
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
                    resultados.append({"id_producto": id_producto, "nueva_cantidad": nueva_cantidad})
        return resultados

    async def fillPedidos():
        pedidos_data = await getPedidosEntrantes()
        set_pedidos(pedidos_data)

    async def handle_rechazar(pedido, motivo):
        json = {
            "motivo": motivo,
            "status": "HISTORIAL"
        }
        await rechazarPedido(pedido, json)
        await fillPedidos()
    def rechazar_button_click_handler(e, pedido_id, motivo):
        async def async_handler():
            await handle_rechazar(pedido_id, motivo)
        asyncio.ensure_future(async_handler())

    async def handle_aceptar(pedido):
        json = {
            "status": "EN CURSO"
        }
        #este de abajo cambia el estado a en curso del pedido, no desactivar hasta que esté ready el desarrollo
        #await aceptarPedido(pedido, json)
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
                        #Aquí ya se sabe que es un pedido que podemos cumplir sin problemas, toda notificar a Logística y ver si ellos pueden rechazar o sí o sí responden y restamos de una el inventario                       
                        newStock = restarStock(detalle, realstock)
                        print(newStock)
                        await actualizarStock(newStock)
                        await handle_aceptar(pedido_id)
                    else:
                        print("Stock insuficiente, se requiere producir.")
        asyncio.ensure_future(async_handler())

    use_effect(fillPedidos)

    def render_detalle_pedido(pedido_item):
        return html.div(
            {
                "key": pedido_item["detalle_pedido"]["id"],
                "class": "card card-body mb-2"
            },
            html.div(
                {"class": "card-body"},
                html.div({"class": "card-title"},
                         f"Producto: {pedido_item['producto']['nombre']}"),
                html.p(
                    f"Cantidad: {pedido_item['detalle_pedido']['cantidad']}")
            )
        )

    grouped_pedidos = {}
    id_productos = {}
    for pedido_item in pedidos:
        pedido_id = pedido_item["pedido"]["id"]
        if pedido_id not in grouped_pedidos:
            grouped_pedidos[pedido_id] = []
        if pedido_id not in id_productos:
            id_productos[pedido_id] = []
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
                                               "onclick": lambda e, pedido_id=pedido_id: aceptar_button_click_handler(e, pedido_id)#lambda e, pedido_id=pedido_id: aceptar_button_click_handler(e, pedido_id, id_productos)
                                               },
                                              "Aceptar"
                                              ),
                                  #html.button({"class": "btn btn-danger",
                                               #"onclick": lambda e, pedido_id=pedido_id: rechazar_button_click_handler(e, pedido_id, motivo)
                                               #},
                                              #"Rechazar"
                                              #)
                     )),
            html.div({"class": "input-centrado"},
                     html.input(
                {
                    "type": "text",
                    "placeholder": "Motivo en caso de rechazo...",
                    "onChange": lambda e: set_motivo(e["target"]["value"])
                }
            )),
            [render_detalle_pedido(pedido_item)
             for pedido_item in grupo_pedidos]
        )
        )
    return html.div(
        html.h2({"class": "titulo-pantalla"}, "PEDIDOS ENTRANTES"),
        html.div({"class": "pedidos-container"}, cards)
    )
