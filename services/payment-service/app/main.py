from fastapi import FastAPI
import asyncio

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/pay")
async def pay():
    await asyncio.sleep(0.2)
    return {"status": "paid"}