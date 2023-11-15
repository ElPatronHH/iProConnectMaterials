from reactpy import html, component

@component
def HistorialComprasContent():
    
    return html.div(
        html.div(
            html.h2({"class":"titulo-pantalla"},"HISTORIAL DE COMPRAS")),
        html.div({"class": "pedidos-container"},)
    )