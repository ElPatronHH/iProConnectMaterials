from reactpy import html, component, use_state, use_effect
from database.api import getPedidosEntrantes, rechazarPedido
import asyncio


@component
def PedidosEntrantesContent():
    pedidos, set_pedidos = use_state([])
    motivo, set_motivo = use_state("")

    async def fillPedidos():
        pedidos_data = await getPedidosEntrantes()
        set_pedidos(pedidos_data)

    async def handle_rechazar(pedido):
        await rechazarPedido(pedido)
        await fillPedidos()

    def rechazar_button_click_handler(e, pedido_id):
        async def async_handler():
            await handle_rechazar(pedido_id)
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
                                                            # "onclick": lambda event: delete_product(stock_item["id"])
                                                            },
                                                           "Aceptar"
                                                           ),
                                               html.button({"class": "btn btn-danger",
                                                            "onclick": lambda e, pedido_id=pedido_id: rechazar_button_click_handler(e, pedido_id)
                                                            },
                                                           "Rechazar"
                                                           )
                                               )),
                              html.div({"class": "input-centrado"},
                                       html.input(
                                  {
                                      "type": "text",
                                      "placeholder": "Motivo en caso de rechazo...",
                                      "value": motivo
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
