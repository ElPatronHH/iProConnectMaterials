from reactpy import html

Topbar = (
    html.header(
        html.ul(
            html.li(
                html.a({"href": "/"},
                       "iProConnectMaterials")),
            html.li(
                html.a({"href": "/pedidosentrantes"},
                       "Pedidos Entrantes")),
            html.li(
                html.a({"href": "/pedidosencurso"},
                       "Pedidos en Curso")),
            html.li(
                html.a({"href": "/historialpedidos"},
                       "Historial de Pedidos")),
            html.li(
                html.a({"href": "/inventarios"},
                       "Inventarios")),
            html.li(
                html.a({"href": "/ajustes"},
                       "Ajustes")),
        )
    )
)
