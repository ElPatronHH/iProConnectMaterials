import httpx
direccion = "http://localhost:8000"
#direccion = "http://iproconnectmaterials.eastus.cloudapp.azure.com:8000"

async def getStock():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{direccion}/backend/stockfull")
    if response.status_code == 200:
        result = response.json()
        return result

async def getPedidosEntrantes():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{direccion}/backend/pedidosEntrantes")
    if response.status_code == 200:
        result = response.json()
        return result
    
async def getHistorialDePedidos():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{direccion}/backend/historialDePedidos")
    if response.status_code == 200:
        result = response.json()
        return result
    
async def getDePedidosEnCurso():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{direccion}/backend/pedidosEnCurso")
    if response.status_code == 200:
        result = response.json()
        return result
    
async def deleteProducto(stock_id):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{direccion}/stock/{stock_id}")
    if response.status_code == 200:
        return True  
    else:
        return False  
    
async def deleteProductoLogico(producto_id):
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{direccion}/backend/productos/{producto_id}/cambiar-status?new_status=0")
    if response.status_code == 200:
        return True  
    else:
        return False 
    
async def modifyProducto(producto_id, update_data):
    async with httpx.AsyncClient() as client:
        url = f"{direccion}/backend/productos/{producto_id}"
        response = await client.put(url, json=update_data) 
    if response.status_code == 200:
        return True
    else:
        return False

async def addProducto(producto_data):
    url = f"{direccion}/backend/addproduct" 
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=producto_data)
    if response.status_code == 201:
        return response.json()
    
async def rechazarPedido(pedido_id,update_data):
    url = f"{direccion}/backend/pedidos/{pedido_id}" 
    async with httpx.AsyncClient() as client:
        response = await client.put(url, json=update_data)
    if response.status_code == 200:
        return True
    else:
        return False
    
async def aceptarPedido(pedido_id,update_data):
    url = f"{direccion}/backend/acceptpedido/{pedido_id}" 
    async with httpx.AsyncClient() as client:
        response = await client.put(url, json=update_data)
    if response.status_code == 200:
        return True
    else:
        return False
    
import httpx

async def comprobarStockSuficiente(id_productos):
    url = f"{direccion}/backend/comprobacion_stock"
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=id_productos)
    if response.status_code == 200:
        return response.json()
    else:
        return False
    
async def obtenerDetalleDePedidos(id_pedido):
    url = f"{direccion}/backend/detalle_pedidos?pedido_id={id_pedido}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

async def modifyStock(producto_id, update_data):
    async with httpx.AsyncClient() as client:
        url = f"{direccion}/backend/productos_new_stock/{producto_id}"
        response = await client.put(url, json=update_data) 
    if response.status_code == 200:
        return response.json()
    else:
        return False
    
async def getItemFabricacion(producto_id):
    url = f"{direccion}/backend/producto_tiempo/{producto_id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Error al obtener datos para el producto {producto_id}"}

async def getCompras():
    url = f"{direccion}/backend/gethistorialCompras"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"Error al obtener datos."}
    
async def addCompra(compra_data):
    url = f"{direccion}/backend/compras_logs" 
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=compra_data)
    if response.status_code == 201:
        return response.json()