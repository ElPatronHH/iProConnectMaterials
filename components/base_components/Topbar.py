from reactpy import html

Topbar = (
    html.header(
        html.h2(
            "iProConnectMaterials"),
        html.nav({"class": "topbar"},
                 
            html.a({"href": "/pedidosentrantes"},
                   "Pedidos Entrantes"),
            html.a({"href": "/pedidosencurso"},
                   "Pedidos en Curso"),
            html.a({"href": "/historialpedidos"},
                   "Historial de Pedidos"),
            html.a({"href": "/inventarios"},
                   "Inventarios"),
            html.a({"href": "/compras"},
                   "Compras"),
        )
    )
)
