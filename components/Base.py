from reactpy import html
from components.base_components.Head import Head 
from components.base_components.Topbar import Topbar
#sidebar, footer

def Base(content, context_value):

    return html.main(
        Head,
#        sidebar,
        Topbar,
        content
#        footer
    )