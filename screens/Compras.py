from reactpy import component
from reactpy.core.hooks import use_context
from components.Base import Base

from content.ComprasContent import ComprasContent

@component
def Compras(context):
    context_value = use_context(context)

    return Base((ComprasContent()), context_value)