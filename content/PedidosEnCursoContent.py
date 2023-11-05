from reactpy import html, component, use_state, use_effect
from database.api import getPedidosEntrantes


@component
def PedidosEnCursoContent():
    pedidos, set_pedidos = use_state([])

    async def fillItems():
        pedidos_data = await getPedidosEntrantes()
        set_pedidos(pedidos_data)

    use_effect(fillItems, [])

    def accept_pedido(pedido_id):
        print("Pedido Aceptado.")

    def reject_pedido(pedido_id):
        print("Pedido Rechazado.")

    def render_pedidosEntrantes_item(pedido_item):
        return html.div(
            {
                "key": pedido_item["id"],
                "class": "card card-body mb-2"
            },
            html.div(
                {"class": "card-body"},
                html.h5({"class": "card-title"},
                        f"Pedido ID: {pedido_item['id']}"),
                html.p(f"ID Producto: {pedido_item['producto_id']}"),
                html.p(f"Cantidad: {pedido_item['cantidad']}"),
                html.p(f"Fecha del pedido: {pedido_item['fecha_pedido']}"),
                html.p(
                    f"Fecha de entrega solicitada: {pedido_item['fecha_entrega']}"),
                html.p(f"Método de pago: {pedido_item['metodo_pago']}"),
                html.div({"class":"botonera-card"},
                html.button(
                    {
                        "class": "btn btn-primary",
                        "onclick": lambda event: accept_pedido(pedido_item['id'])
                    },
                    "Aceptar"
                ),
                html.button(
                    {
                        "class": "btn btn-danger",
                        "onclick": lambda event: reject_pedido(pedido_item['id'])
                    },
                    "Rechazar"
                ))
            ),

        )

    return html.div(
        html.h2({"class":"titulo-pantalla"},"PEDIDOS EN CURSO"),
        html.div({"class": "pedidos-container"}, [render_pedidosEntrantes_item(pedido_item)
                 for pedido_item in pedidos])
    )
