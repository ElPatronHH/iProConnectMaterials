from reactpy import component
from reactpy.core.hooks import use_context
from components.Base import Base

from content.InventariosContent import InventariosContent


@component
def Inventarios(context):
    context_value = use_context(context)

    return Base((InventariosContent()), context_value)