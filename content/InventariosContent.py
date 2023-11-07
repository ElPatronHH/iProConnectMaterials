from reactpy import html, component, use_state, use_effect
from database.api import getStock, deleteProducto
import asyncio


@component
def InventariosContent():
    stock, set_stock = use_state([])

    async def fillItems():
        stock_data = await getStock()
        set_stock(stock_data)

    async def handle_delete(producto):
        await deleteProducto(producto)
        await fillItems()

    def delete_button_click_handler(e, producto_id):
        async def async_handler():
            await handle_delete(producto_id)
        asyncio.ensure_future(async_handler())
    use_effect(fillItems)

    def render_stock_item(stock_item):
        return html.div(
            {
                "key": stock_item["id"],
                "class": "card card-body mb-2"
            },
            html.p({"class": "card-title"}, stock_item["nombre"]),
            html.p({"class": "centered-p"}, f"{stock_item['descripcion']}"),
            html.p(f"ID: {stock_item['id']}"),
            html.p(f"Medida: {stock_item['medida']}"),
            html.p(f"Stock: {stock_item['stock']}"),
            html.p(f"Precio de compra: {stock_item['precio_compra']}"),
            html.p(f"Precio de venta: {stock_item['precio_venta']}"),
            html.p(f"Cantidad Máxima Stock: {stock_item['cantidad_max']}"),
            html.p(f"Cantidad Mínima Stock: {stock_item['cantidad_min']}"),
            html.p(f"Venta Máxima: {stock_item['venta_max']}"),
            html.p(f"Venta Mínima: {stock_item['venta_min']}"),
            html.div({"class": "botonera-card"},
                     html.button({"class": "btn",
                                  # "onclick": lambda event: delete_product(stock_item["id"])
                                  },
                                 "Modificar"
                                 ),
                     html.button({"class": "btn btn-danger",
                                  "onclick": lambda e: delete_button_click_handler(e, stock_item["id"])
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
