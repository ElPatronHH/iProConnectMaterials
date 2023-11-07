from reactpy import html, component, use_state, use_effect
from database.api import getPedidosEntrantes

@component
def PedidosEntrantesContent():
    pedidos, set_pedidos = use_state([])

    async def fillItems():
        pedidos_data = await getPedidosEntrantes()
        set_pedidos(pedidos_data)

    use_effect(fillItems, [])

    def accept_pedido(id_pedido):
        print(f"Pedido Aceptado: {id_pedido}")

    def reject_pedido(id_pedido):
        print(f"Pedido Rechazado: {id_pedido}")

    def render_detalle_pedido(detalle_pedido):
        return html.div(
            {"class": "detalle-pedido"},
            html.p(f"Producto: {detalle_pedido['producto']['nombre']}"),
            html.p(f"Precio Unitario: ${detalle_pedido['precio']}"),  # Cambio aquí
        )

    def render_pedidosEntrantes_item(pedido_item):
        detalles_pedido = pedido_item['detalle_pedido']
        return html.div(
            {
                "key": pedido_item["pedido"]["id"],
                "class": "card card-body mb-2"
            },
            html.div(
                {"class": "card-body"},
                html.div({"class": "card-title"},
                         f"ID del Pedido: {pedido_item['pedido']['id']}"),
                html.p(f"Fecha del Pedido: {pedido_item['pedido']['fecha_pedido']}"),
                html.p(f"Fecha de Entrega Deseada: {pedido_item['pedido']['fecha_entrega']}"),
                html.p(f"Método de Pago: {pedido_item['pedido']['metodo_pago']}"),
                html.p(f"Total: ${pedido_item['pedido']['total']}"),
                html.div({"class": "detalle-pedido-container"},
                    [render_detalle_pedido(detalle) for detalle in detalles_pedido]
                ),
                html.div({"class": "botonera-card"},
                     html.button({"class": "btn btn-primary",
                                  #"onclick": lambda event: accept_pedido(pedido_item['pedido']['id'])
                                  },
                                 "Aceptar"
                                 ),
                     html.button({"class": "btn btn-danger",
                                  #"onclick": lambda event: reject_pedido(pedido_item['pedido']['id'])
                                  },
                                 "Rechazar"
                                 )
                     )
            )
        )

    return html.div(
        html.h2({"class": "titulo-pantalla"}, "PEDIDOS ENTRANTES"),
        html.div({"class": "pedidos-container"},
                 [render_pedidosEntrantes_item(pedido_item) for pedido_item in pedidos])
    )



    
    
    """
    def render_pedidosEntrantes_item(pedido_item):
        return html.div(
            {
                "key": pedido_item["id"],
                "class": "card card-body mb-2"
            },
            html.div(
                {"class": "card-body"},
                html.div({"class": "card-title"},
                         f"Producto: {pedido_item['producto_id']}"),
                html.p(f"Cantidad: {pedido_item['cantidad']}"),
            )
        )

    grouped_pedidos = {}
    for pedido_item in pedidos:
        pedido_id = pedido_item["pedido_id"]
        if pedido_id not in grouped_pedidos:
            grouped_pedidos[pedido_id] = []
        grouped_pedidos[pedido_id].append(pedido_item)

    cards = []
    for pedido_id, grupo_pedidos in grouped_pedidos.items():
        cards.append(html.div({"class": "grupo-tarjeta"},
                        html.h5({"class": "card-title"},
                                f"Pedido {pedido_id}",
                            html.h5({"class": "card-title2"},
                            html.p(f"Fecha del pedido: {pedido_item ['fecha_pedido']}"),
                            html.p(f"Fecha de entrega solicitada: {pedido_item['fecha_entrega']}"),
                            html.p(f"Método de pago: {pedido_item['metodo_pago']}"),
                            html.div({"class":"botonera-card"},
                            html.button({"class": "btn btn-primary",
                                # "onclick": lambda event: accept_pedido(pedido_item)
                                },
                                "Aceptar"
                            ),
                            html.button({"class": "btn btn-danger",
                                # "onclick": lambda event: reject_pedido(pedido_item)
                                },
                                "Rechazar"
                            )
                        ))),
                    [render_pedidosEntrantes_item(pedido_item)
                    for pedido_item in grupo_pedidos]
                    )
        )

    return html.div(
        html.h2({"class": "titulo-pantalla"}, "PEDIDOS ENTRANTES"),
        html.div({"class": "pedidos-container"}, cards)
    )"""