from reactpy import html
from sqlalchemy.sql import select
from database.connection import conexion, stock_table  

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
