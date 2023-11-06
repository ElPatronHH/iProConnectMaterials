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
        return html.li(
            {
                "key": stock_item["id"],
                "class": "card card-body mb-2"
            },
            html.p({"class": "card-title"}, stock_item["nombre"]),
            html.p(f"ID: {stock_item['id']}"),
            html.p(f"Descripción: {stock_item['descripcion']}"),
            html.p(f"Precio de compra: {stock_item['precio_compra']}"),
            html.p(f"Precio de venta: {stock_item['precio_venta']}")
        )

    return html.div(
        html.h2({"class":"titulo-pantalla"},"INVENTARIO"),
        html.ul([render_stock_item(stock_item) for stock_item in stock])
    )

