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

app = FastAPI()
app.mount("/CSS", StaticFiles(directory="CSS"), name="CSS")


@component
def Index():
    context = create_context("value")

    return simple.router(
        route("/", App(context)),
        route("/historial_de_pedidos", HistorialPedidos(context)),
        route("/inventarios", Inventarios(context)),
        route("/ajustes", Ajustes(context))
    )

configure(app, Index)