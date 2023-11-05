from reactpy import html, component, use_state, use_effect
from database.api import getPedidosEntrantes

@component
def PedidosEntrantesContent():
    pedidos, set_pedidos = use_state([])

    async def fillItems():
        pedidos_data = await getPedidosEntrantes()
        set_pedidos(pedidos_data)

    use_effect(fillItems)

    def render_pedidosEntrantes_item(pedido_item):
        return html.li(
            {
                "key": pedido_item["id"],
                "class_name": "card card-body mb-2"
            },
            html.p(f"ID: {pedido_item['id']}"),
            html.p(f"ID Producto: {pedido_item['producto_id']}"),
            html.p(f"Cantidad: {pedido_item['cantidad']}"),
            html.p(f"Fecha del pedido: {pedido_item['fecha_pedido']}"),
            html.p(f"Fecha de entrega solicitada:{pedido_item['fecha_entrega']}"),
            html.p(f"Método de pago: {pedido_item['metodo_pago']}"),
        )

    return html.div(
        html.h2("PEDIDOS ENTRANTES"),
        html.ul([render_pedidosEntrantes_item(pedido_item) for pedido_item in pedidos])
    )

