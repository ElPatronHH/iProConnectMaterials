from reactpy import html, component, use_state, use_effect
from database.api import getDePedidosEnCurso
import asyncio


@component
def PedidosEnCursoContent():
    pedidos, set_pedidos = use_state([])

    async def fillPedidos():
        pedidos_data = await getDePedidosEnCurso()
        set_pedidos(pedidos_data)

    use_effect(fillPedidos)

    def render_detalle_pedido(pedido_item):
        return html.div(
            html.div({
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
            ))

    grouped_pedidos = {}
    for pedido_item in pedidos:
        pedido_id = pedido_item["pedido"]["id"]
        if pedido_id not in grouped_pedidos:
            grouped_pedidos[pedido_id] = {
                "pedido_item": pedido_item, "productos": []}
        grouped_pedidos[pedido_id]["productos"].append(pedido_item)

    cards = []
    for pedido_id, pedido_data in grouped_pedidos.items():
        motivo = pedido_data["pedido_item"].get(
            "pedido", {}).get("motivo", "Motivo no especificado")
        cards.append(html.div({"class": "grupo-tarjeta"},
                              html.h5({"class": "card-title"},
                                      f"Pedido {pedido_id} RECHAZADO" if motivo else f"PEDIDO {pedido_id}",
                                      html.p(
                                  f"Fecha: {pedido_item['pedido']['fecha_entrega']}")),
                              html.p({"class": "centered-p"},
                                     motivo) if motivo else "",
                              [render_detalle_pedido(pedido_item)
                               for pedido_item in pedido_data["productos"]]
                              )
                     )

    return html.div(
        html.h2({"class": "titulo-pantalla"}, "PEDIDOS EN CURSO"),
        html.div({"class": "pedidos-container"}, cards)
    )
