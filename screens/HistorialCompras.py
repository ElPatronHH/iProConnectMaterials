from reactpy import component
from reactpy.core.hooks import use_context
from components.Base import Base

from content.HistorialComprasContent import HistorialComprasContent

@component
def HistorialCompras(context):
    context_value = use_context(context)

    return Base((HistorialComprasContent()), context_value)