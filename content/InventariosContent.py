from reactpy import html, component, use_state, use_effect
from database.api import getStock


@component
def InventariosContent():
    stock, set_stock = use_state([])

    async def fillItems():
        stock_data = await getStock()
        set_stock(stock_data)

    use_effect(fillItems)

    def render_stock_item(stock_item):
        return html.div(
            {
                "key": stock_item["id"],
                "class": "card card-body mb-2"
            },
            html.p({"class": "card-title"}, stock_item["nombre"]),
            html.p({"class": "centered-p"}, f"{stock_item['descripcion']}"),
            html.p(f"ID {stock_item['id']}"),
            html.p(f"Precio de compra: {stock_item['precio_compra']}"),
            html.p(f"Precio de venta: {stock_item['precio_venta']}"),
            html.div({"class": "botonera-card"},
                     html.button({"class": "btn btn-primary",
                                  # "onclick": lambda event: accept_pedido(pedido_item)
                                  },
                                 "Modificar"
                                 ),
                     html.button({"class": "btn btn-danger",
                                  # "onclick": lambda event: reject_pedido(pedido_item)
                                  },
                                 "Eliminar"
                                 )
                     )
        )

    return html.div(
        html.h2({"class": "titulo-pantalla"}, "INVENTARIO"),
        html.div({"class": "pedidos-container"},
                 html.div(
            {
                "class": "cardv2"
            },
                     html.button({"class": "btn btn-primary",
                                  # "onclick": lambda event: accept_pedido(pedido_item)
                                  },
                                 "Añadir Producto"
                                 )
        ),
                 [render_stock_item(stock_item) for stock_item in stock]),
        )
