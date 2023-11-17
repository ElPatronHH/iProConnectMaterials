from reactpy import html, component
from reactpy import html, component, use_state, use_effect
from database.api import getCompras, rechazarPedido
import asyncio

@component
def HistorialComprasContent():
    compras, set_compras = use_state([])

    async def fillCompras():
        compras_data = await getCompras()
        set_compras(compras_data)

    use_effect(fillCompras)

    def render_historial_compras(compra_item):
        return html.tr(
            {"key": compra_item["compra"]["id"]},
            html.td(f"{compra_item['compra']['fecha']}"),
            html.td(f"{compra_item['producto']['nombre']}"),
            html.td(f"{compra_item['producto']['descripcion']}"),
            html.td(f"{compra_item['producto']['id']}"),
            html.td(f"{compra_item['compra']['precio_total']}")
        )

    return html.div(
        html.div(
            html.h2({"class": "titulo-pantalla"}, "HISTORIAL DE COMPRAS")),
        html.table(
            {"class": "table table-striped"},
            html.thead(
                html.tr(
                    html.th("Fecha"),
                    html.th("Parte comprada"),
                    html.th("Descripción"),
                    html.th("Cantidad"),
                    html.th("Costo Total")
                )
            ),
            html.tbody([render_historial_compras(compra_item) for compra_item in compras])
        )
    )
