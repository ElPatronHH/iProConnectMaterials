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
                "class_name": "card card-body mb-2"
            },
            html.p({"class_name": "fw-bold h3"}, stock_item["descripcion"]),
            html.p(f"ID: {stock_item['id']}"),
            html.p(f"Stock actual: {stock_item['currentStock']}"),
            html.p(f"Stock mínimo para la venta: {stock_item['minVenta']}"),
            html.p(f"Punto de reorden: {stock_item['puntoReorden']}"),
            html.p(f"Stock máximo para la venta: {stock_item['maxVenta']}")
        )

    return html.div(
        html.h2("INVENTARIO"),
        html.ul([render_stock_item(stock_item) for stock_item in stock])
    )


"""
sel = select(stock_table.c.id, stock_table.c.numParte, stock_table.c.descripcion, stock_table.c.currentStock)
resultados = conexion.execute(sel)  

table = html.table({"class":"table"},
    html.thead(
        html.tr(
            html.th("ID"),
            html.th("Número de Parte"),
            html.th("Descripción"),
            html.th("Stock actual"),
            
        ),
    ),
    html.tbody(
        [
            html.tr(
                html.td(fila[0]), 
                html.td(fila[1]), 
                html.td(fila[2]),  
                html.td(fila[3]),
            )
            for fila in resultados
        ],
    ),
)

InventariosContent = html.div(
    html.h2("INVENTARIO"),
    table
)
"""
