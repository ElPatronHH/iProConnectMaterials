import httpx
direccion = "http://localhost:8000"
#direccion = "http://iproconnectmaterials.eastus.cloudapp.azure.com:8000"

async def getStock():
    async with httpx.AsyncClient() as client:
<<<<<<< Updated upstream
        response = await client.get("http://40.76.247.213:8000/backend/stockfull")
=======
        response = await client.get(f"{direccion}/backend/stockfull")
>>>>>>> Stashed changes
    if response.status_code == 200:
        result = response.json()
        return result

async def getPedidosEntrantes():
    async with httpx.AsyncClient() as client:
<<<<<<< Updated upstream
        response = await client.get("http://40.76.247.213:8000/backend/pedidosEntrantes")
=======
        response = await client.get(f"{direccion}/backend/pedidosEntrantes")
>>>>>>> Stashed changes
    if response.status_code == 200:
        result = response.json()
        return result
    
async def getHistorialDePedidos():
    async with httpx.AsyncClient() as client:
<<<<<<< Updated upstream
        response = await client.get("http://40.76.247.213:8000/backend/historialDePedidos")
=======
        response = await client.get(f"{direccion}/backend/historialDePedidos")
>>>>>>> Stashed changes
    if response.status_code == 200:
        result = response.json()
        return result
    
async def getDePedidosEnCurso():
    async with httpx.AsyncClient() as client:
<<<<<<< Updated upstream
        response = await client.get("http://40.76.247.213:8000/backend/pedidosEnCurso")
=======
        response = await client.get(f"{direccion}/backend/pedidosEnCurso")
>>>>>>> Stashed changes
    if response.status_code == 200:
        result = response.json()
        return result
    
async def deleteProducto(stock_id):
    async with httpx.AsyncClient() as client:
<<<<<<< Updated upstream
        response = await client.delete(f"http://40.76.247.213:8000/stock/{stock_id}")
=======
        response = await client.delete(f"{direccion}/stock/{stock_id}")
>>>>>>> Stashed changes
    if response.status_code == 200:
        return True  
    else:
        return False  
    
async def deleteProductoLogico(producto_id):
    async with httpx.AsyncClient() as client:
<<<<<<< Updated upstream
        response = await client.put(f"http://40.76.247.213:8000/backend/productos/{producto_id}/cambiar-status?new_status=0")
=======
        response = await client.put(f"{direccion}/backend/productos/{producto_id}/cambiar-status?new_status=0")
>>>>>>> Stashed changes
    if response.status_code == 200:
        return True  
    else:
        return False 
    
async def modifyProducto(producto_id, update_data):
    async with httpx.AsyncClient() as client:
<<<<<<< Updated upstream
        url = f"http://40.76.247.213:8000/backend/productos/{producto_id}"
=======
        url = f"{direccion}/backend/productos/{producto_id}"
>>>>>>> Stashed changes
        response = await client.put(url, json=update_data) 
    if response.status_code == 200:
        return True
    else:
        return False

async def addProducto(producto_data):
<<<<<<< Updated upstream
    url = "http://40.76.247.213:8000/backend/addproduct" 
=======
    url = f"{direccion}/backend/addproduct" 
>>>>>>> Stashed changes
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=producto_data)
    if response.status_code == 201:
        return response.json()
    
async def rechazarPedido(pedido_id,update_data):
<<<<<<< Updated upstream
    url = f"http://40.76.247.213:8000/backend/pedidos/{pedido_id}" 
=======
    url = f"{direccion}/backend/pedidos/{pedido_id}" 
>>>>>>> Stashed changes
    async with httpx.AsyncClient() as client:
        response = await client.put(url, json=update_data)
    if response.status_code == 200:
        return True
    else:
        return False
    
async def aceptarPedido(pedido_id,update_data):
<<<<<<< Updated upstream
    url = f"http://40.76.247.213:8000/backend/acceptpedido/{pedido_id}" 
=======
    url = f"{direccion}/backend/acceptpedido/{pedido_id}" 
>>>>>>> Stashed changes
    async with httpx.AsyncClient() as client:
        response = await client.put(url, json=update_data)
    if response.status_code == 200:
        return True
    else:
        return False
    
import httpx

async def comprobarStockSuficiente(id_productos):
<<<<<<< Updated upstream
    url = "http://40.76.247.213:8000/backend/comprobacion_stock"
=======
    url = f"{direccion}/backend/comprobacion_stock"
>>>>>>> Stashed changes
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=id_productos)
    if response.status_code == 200:
        return response.json()
    else:
        return False
    
async def obtenerDetalleDePedidos(id_pedido):
<<<<<<< Updated upstream
    url = f"http://40.76.247.213:8000/backend/detalle_pedidos?pedido_id={id_pedido}"
=======
    url = f"{direccion}/backend/detalle_pedidos?pedido_id={id_pedido}"
>>>>>>> Stashed changes
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

async def modifyStock(producto_id, update_data):
    async with httpx.AsyncClient() as client:
<<<<<<< Updated upstream
        url = f"http://40.76.247.213:8000/backend/productos_new_stock/{producto_id}"
=======
        url = f"{direccion}/backend/productos_new_stock/{producto_id}"
>>>>>>> Stashed changes
        response = await client.put(url, json=update_data) 
    if response.status_code == 200:
        return response.json()
    else:
        return False
    
async def getItemFabricacion(producto_id):
<<<<<<< Updated upstream
    url = f"http://40.76.247.213:8000/backend/producto_tiempo/{producto_id}"
=======
    url = f"{direccion}/backend/producto_tiempo/{producto_id}"
>>>>>>> Stashed changes
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Error al obtener datos para el producto {producto_id}"}

async def getCompras():
<<<<<<< Updated upstream
    url = f"http://40.76.247.213:8000/backend/gethistorialCompras"
=======
    url = f"{direccion}/backend/gethistorialCompras"
>>>>>>> Stashed changes
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"Error al obtener datos."}
    
async def addCompra(compra_data):
<<<<<<< Updated upstream
    url = "http://40.76.247.213:8000/backend/compras_logs" 
=======
    url = f"{direccion}/backend/compras_logs" 
>>>>>>> Stashed changes
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=compra_data)
    if response.status_code == 201:
        return response.json()