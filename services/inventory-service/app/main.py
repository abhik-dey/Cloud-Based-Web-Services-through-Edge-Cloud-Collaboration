from fastapi import FastAPI
import threading
import asyncio

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

seats = 100
seats_lock = threading.Lock()

@app.get("/check")
async def check():
    await asyncio.sleep(0.1)
    with seats_lock:
        return {"seats": seats}

@app.post("/consume")
async def consume():
    global seats
    with seats_lock:
        if seats > 0:
            seats -= 1
        return {"seats": seats}