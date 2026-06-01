from fastapi import FastAPI
from app.service import process_booking

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["*"],
)

@app.post("/book")
async def book():
    return await process_booking()