import httpx

async def getStock():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/stockfull")

    if response.status_code == 200:
        result = response.json()
        return result
    
async def getPedidosEntrantes():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/backend/pedidosEntrantes")

    if response.status_code == 200:
        result = response.json()
        return result