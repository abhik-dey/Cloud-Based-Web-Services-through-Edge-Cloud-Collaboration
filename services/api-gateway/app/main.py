from fastapi import FastAPI, Request, HTTPException
import httpx
import asyncio
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BOOKING_URL = "http://booking-service:8000/book"

# Global state for simulation
SIMULATION_CONFIG = {
    "cloud_mode": True
}

class ConfigUpdate(BaseModel):
    cloud_mode: bool

@app.get("/config")
def get_config():
    return SIMULATION_CONFIG

@app.post("/config")
def update_config(config: ConfigUpdate):
    SIMULATION_CONFIG["cloud_mode"] = config.cloud_mode
    return SIMULATION_CONFIG

@app.post("/book")
async def route_booking(request: Request):
    if SIMULATION_CONFIG["cloud_mode"]:
        # SIMULATING CLOUD LATENCY
        # A 200ms delay to simulate the "Network Hop" of the Edge talking to the centralized Cloud services
        await asyncio.sleep(0.200)
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(BOOKING_URL, timeout=10.0)
            response.raise_for_status()
            return response.json()
    except httpx.ConnectError:
        raise HTTPException(status_code=503, detail="Booking service unavailable")
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Booking service timed out")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))

