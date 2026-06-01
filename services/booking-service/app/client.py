import httpx
from fastapi import HTTPException

INVENTORY_URL = "http://inventory-service:8000/check"
INVENTORY_CONSUME_URL = "http://inventory-service:8000/consume"
PAYMENT_URL = "http://payment-service:8000/pay"

async def check_inventory() -> int:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(INVENTORY_URL, timeout=10.0)
            response.raise_for_status()
            return response.json()["seats"]
        except httpx.ConnectError:
            raise HTTPException(status_code=503, detail="Inventory service unavailable")
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="Inventory service timed out")
        except (KeyError, ValueError):
            raise HTTPException(status_code=502, detail="Unexpected response from inventory service")

async def consume_seat():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(INVENTORY_CONSUME_URL, timeout=10.0)
            response.raise_for_status()
        except httpx.ConnectError:
            raise HTTPException(status_code=503, detail="Inventory service unavailable")
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="Inventory service timed out")

async def make_payment():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(PAYMENT_URL, timeout=10.0)
            response.raise_for_status()
        except httpx.ConnectError:
            raise HTTPException(status_code=503, detail="Payment service unavailable")
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="Payment service timed out")