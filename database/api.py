import httpx

async def getStock():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/backend/stockfull")

    if response.status_code == 200:
        result = response.json()
        return result

async def getPedidosEntrantes():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/backend/pedidosEntrantes")

    if response.status_code == 200:
        result = response.json()
        return result
    
async def getHistorialDePedidos():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/backend/historialDePedidos")

    if response.status_code == 200:
        result = response.json()
        return result
    
async def deleteProducto(stock_id):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"http://localhost:8000/stock/{stock_id}")
    if response.status_code == 200:
        return True  
    else:
        return False  
    
async def deleteProductoLogico(producto_id):
    async with httpx.AsyncClient() as client:
        response = await client.put(f"http://localhost:8000/backend/productos/{producto_id}/cambiar-status?new_status=0")
    if response.status_code == 200:
        return True  
    else:
        return False 

async def rechazarPedido(pedido_id):
    url = f"http://localhost:8000/backend/pedidos/{pedido_id}/cambiar-status?new_status=HISTORIAL" 
    data = {"status": "HISTORIAL"}
    async with httpx.AsyncClient() as client:
        response = await client.put(url, json=data)
    if response.status_code == 200:
        return True
    else:
        return False

async def addProducto(producto_data):
    url = "http://localhost:8000/backend/addproduct" 
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=producto_data)

    if response.status_code == 201:
        return response.json()

