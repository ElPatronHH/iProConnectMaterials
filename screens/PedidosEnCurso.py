from reactpy import component
from reactpy.core.hooks import use_context
from components.Base import Base

from content.PedidosEnCursoContent import PedidosEnCursoContent

@component
def PedidosEnCurso(context):
    context_value = use_context(context)
    
    return Base((PedidosEnCursoContent()), context_value)