from fastapi import FastAPI
from reactpy.backend.fastapi import configure
from reactpy import component, html
from fastapi.staticfiles import StaticFiles
from reactpy.core.hooks import create_context
from reactpy_router import route, simple

# Content
from screens.App import App
from screens.HistorialPedidos import HistorialPedidos
from screens.Inventarios import Inventarios
from screens.Ajustes import Ajustes
from screens.PedidosEntrantes import PedidosEntrantes
from screens.PedidosEnCurso import PedidosEnCurso

from database.controladores import router as router_api

app = FastAPI()
app.mount("/CSS", StaticFiles(directory="CSS"), name="CSS")

@component
def Index():
    context = create_context("value")

    return simple.router(
        route("/", App(context)),
        route("/pedidosentrantes", PedidosEntrantes(context)),
        route("/pedidosencurso", PedidosEnCurso(context)),
        route("/historialpedidos", HistorialPedidos(context)),
        route("/inventarios",Inventarios(context)),  # Añade await aquí
        route("/ajustes", Ajustes(context))
    )

app.include_router(router_api)

configure(app, Index)