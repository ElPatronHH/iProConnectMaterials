from reactpy import html, component, use_state, use_effect
from database.api import getStock, deleteProductoLogico, modifyProducto  # Importa la función modifyProducto si aún no lo has hecho
import asyncio

@component
def InventariosContent():
    stock, set_stock = use_state([])
    editing_item_id, set_editing_item_id = use_state(None)
    
    precio_compra, set_precio_compra = use_state(0)
    precio_venta, set_precio_venta = use_state(0)
    cantidad_max, set_cantidad_max = use_state(0)
    cantidad_min, set_cantidad_min = use_state(0)
    venta_max, set_venta_max = use_state(0)
    venta_min, set_venta_min = use_state(0)
    
    #Esto renderiza nuestro catálogo
    async def fillItems():
        stock_data = await getStock()
        set_stock(stock_data)

    # Para borrar lógicamente un producto (0 en status)
    async def handle_delete(producto):
        await deleteProductoLogico(producto)
        await fillItems()
    def delete_button_click_handler(e, producto_id):
        async def async_handler():
            await handle_delete(producto_id)
        asyncio.ensure_future(async_handler())

    async def handle_modify(producto):
        # Llama a la función modifyProducto para enviar los datos modificados al servidor
        new_data = {
            "precio_compra": precio_compra,
            "precio_venta": precio_venta,
            "cantidad_max": cantidad_max,
            "cantidad_min": cantidad_min,
            "venta_max": venta_max,
            "venta_min": venta_min
        }
        await modifyProducto(producto, new_data)
        await fillItems()  # Recarga los elementos
        
    def modify_button_click_handler(producto_id,precio_compra,precio_venta,cantidad_max,cantidad_min,venta_max,venta_min):
        set_editing_item_id(producto_id)
        set_precio_compra(precio_compra)
        set_precio_venta(precio_venta)
        set_cantidad_max(cantidad_max)
        set_cantidad_min(cantidad_min)
        set_venta_max (venta_max)
        set_venta_min(venta_min)
    
    # Guarda los cambios
    def save_button_click_handler(producto_id):
        set_editing_item_id(None)  
        async def async_handler():
            await handle_modify(producto_id)
        asyncio.ensure_future(async_handler())
        
    def cancel_button_click_handler():
        set_editing_item_id(None)
        
    use_effect(fillItems)

    def render_stock_item(stock_item):
        is_editing = editing_item_id == stock_item["id"]
        if is_editing: 
            return html.div(
                {
                    "key": stock_item["id"],
                    "class": "card card-body mb-2"
                },
                html.p({"class": "card-title"}, stock_item["nombre"]),
                html.p({"class": "centered-p"}, f"{stock_item['descripcion']}"),
                html.p(f"ID: {stock_item['id']}"),
                html.p(f"Medida: {stock_item['medida']}"),
                html.p(f"Stock: {stock_item['stock']}"),
                html.p("Precio de compra: ",
                    html.input(
                        {
                            "type": "text",
                            "value":  stock_item["precio_compra"],
                            "onChange": lambda e: set_precio_compra(e["target"]["value"])
                        }
                    )
                ),
                html.p(f"Precio de venta: ",
                    html.input(
                        {
                            "type": "text",
                            "value": stock_item["precio_venta"],
                            "onChange": lambda e: set_precio_venta(e["target"]["value"])
                        }
                    )
                ),
                html.p(f"Cantidad Máxima Stock: ",
                    html.input(
                        {
                            "type": "text",
                            "value": stock_item["cantidad_max"],
                            "onChange": lambda e: set_cantidad_max(e["target"]["value"])
                        }
                    )
                ),
                html.p(f"Cantidad Mínima Stock: ",
                    html.input(
                        {
                            "type": "text",
                            "value": stock_item["cantidad_min"],
                            "onChange": lambda e: set_cantidad_min(e["target"]["value"])
                        }
                    )
                ),
                html.p(f"Venta Máxima: ",
                    html.input(
                        {
                            "type": "text",
                            "value": stock_item["venta_max"],
                            "onChange": lambda e: set_venta_max(e["target"]["value"])
                        }
                    )
                ),
                html.p(f"Venta Mínima: ",
                    html.input(
                        {
                            "type": "text",
                            "value": stock_item["venta_min"],
                            "onChange": lambda e: set_venta_min(e["target"]["value"])
                        }
                    )
                ),
                html.div({"class": "botonera-card"},
                        html.button({"class": "btn",
                                    "onclick": lambda e: save_button_click_handler(stock_item["id"])
                                    },
                                    "Guardar"
                                    ),
                        html.button({"class": "btn",
                                    "onclick": lambda e: cancel_button_click_handler()
                                    },
                                    "Cancelar"
                                    )
                        )
            )
        else:
            return html.div(
                {
                    "key": stock_item["id"],
                    "class": "card card-body mb-2"
                },
                html.p({"class": "card-title"}, stock_item["nombre"]),
                html.p({"class": "centered-p"}, f"{stock_item['descripcion']}"),
                html.p(f"ID: {stock_item['id']}"),
                html.p(f"Medida: {stock_item['medida']}"),
                html.p(f"Stock: {stock_item['stock']}"),
                html.p(f"Precio de compra: {stock_item['precio_compra']}"),
                html.p(f"Precio de venta: {stock_item['precio_venta']}"),
                html.p(f"Cantidad Máxima Stock: {stock_item['cantidad_max']}"),
                html.p(f"Cantidad Mínima Stock: {stock_item['cantidad_min']}"),
                html.p(f"Venta Máxima: {stock_item['venta_max']}"),
                html.p(f"Venta Mínima: {stock_item['venta_min']}"),
                html.div({"class": "botonera-card"},
                        html.button({"class": "btn",
                                    "onclick": lambda event: modify_button_click_handler(stock_item["id"], stock_item['precio_compra'],stock_item['precio_venta'],stock_item['cantidad_max'],stock_item['cantidad_min'],stock_item['venta_max'],stock_item['venta_min'])
                                    },
                                    "Modificar"
                                    ),
                        html.button({"class": "btn btn-danger",
                                    "onclick": lambda e: delete_button_click_handler(e, stock_item["id"])
                                    },
                                    "Eliminar"
                                    )
                        )
            )

    return html.div(
        html.h2({"class": "titulo-pantalla"}, "INVENTARIO"),
        html.div({"class": "pedidos-container"},
                 html.div(
            {
                "class": "cardv2"
            },
                     html.button({"class": "btn btn-primary",
                                  # "onclick": lambda event: accept_pedido(pedido_item)
                                  },
                                 "Añadir Producto"
                                 )
        ),
            [render_stock_item(stock_item) for stock_item in stock]
    ))
