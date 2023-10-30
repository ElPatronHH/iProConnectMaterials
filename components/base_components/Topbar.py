from reactpy import html

Topbar = (
    html.header(
        html.ul(
            html.li(
                html.a({"href": "/"},
                       "iProConnectMaterials")),
            html.li(
                html.a({"href": "/historial_de_pedidos"},
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
