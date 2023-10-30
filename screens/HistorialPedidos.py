from reactpy import component
from reactpy.core.hooks import use_context
from components.Base import Base

from content.Main import Main

@component
def HistorialPedidos(context):
    context_value = use_context(context)
    
    return Base((Main), context_value)
