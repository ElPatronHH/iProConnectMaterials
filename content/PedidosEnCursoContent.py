from reactpy import html, component, use_state, use_effect
from database.api import getPedidosEntrantes


@component
def PedidosEnCursoContent():
    
    return html.div(
        html.h2({"class":"titulo-pantalla"},"PEDIDOS EN CURSO"),
        html.div({"class": "pedidos-container"},)
    )
