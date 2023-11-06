from reactpy import component
from reactpy.core.hooks import use_context
from components.Base import Base

from content.PedidosEntrantesContent import PedidosEntrantesContent


@component
def PedidosEntrantes(context):
    context_value = use_context(context)

    return Base((PedidosEntrantesContent()), context_value)