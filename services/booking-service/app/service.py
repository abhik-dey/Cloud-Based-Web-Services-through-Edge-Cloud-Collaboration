import asyncio
import time
from app.client import check_inventory, consume_seat, make_payment

async def process_booking():
    start = time.time()

    try:
        seats = await check_inventory()

        if seats > 0:
            await make_payment()
            await consume_seat()          # Decrement inventory after successful payment
            await asyncio.sleep(0.2)
            return {
                "status": "success",
                "latency": time.time() - start
            }
        else:
            return {"status": "no seats"}
    except Exception as e:
        # Standardize error response to include 'status'
        return {
            "status": "error",
            "detail": str(e),
            "latency": time.time() - start
        }