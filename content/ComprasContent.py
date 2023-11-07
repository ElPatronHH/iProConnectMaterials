from reactpy import html, component

@component
def ComprasContent():
    
    return html.div(
        html.h2({"class":"titulo-pantalla"},"COMPRAS"),
        html.div({"class": "pedidos-container"},)
    )
