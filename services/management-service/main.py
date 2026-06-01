import asyncio
import subprocess
import os
from fastapi import FastAPI, Request, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from typing import List, Dict
import docker

app = FastAPI()
client = docker.from_env()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global process for locust
locust_process = None

@app.get("/services")
async def list_services():
    services = []
    containers = client.containers.list(all=True)
    # Filter for containers in this project (prefix cloud-airline-system)
    for container in containers:
        if container.name.startswith("cloud-airline-system-") or container.name in ["api-gateway", "booking-service", "inventory-service", "payment-service"]:
            services.append({
                "name": container.name,
                "status": container.status,
                "image": container.image.tags[0] if container.image.tags else "unknown"
            })
    return services

@app.post("/services/{name}/start")
async def start_service(name: str):
    try:
        container = client.containers.get(name)
        container.start()
        return {"status": "success", "message": f"Started {name}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/services/{name}/stop")
async def stop_service(name: str):
    try:
        container = client.containers.get(name)
        container.stop()
        return {"status": "success", "message": f"Stopped {name}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/services/{name}/restart")
async def restart_service(name: str):
    try:
        container = client.containers.get(name)
        container.restart()
        return {"status": "success", "message": f"Restarted {name}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/loadtest/start")
async def start_loadtest(users: int = 10, spawn_rate: int = 5):
    global locust_process
    if locust_process and locust_process.poll() is None:
        return {"status": "error", "message": "Load test already running"}
    
    # Run locust headlessly
    cmd = [
        "locust", 
        "-f", "/app/load-testing/locustfile.py", 
        "--headless", 
        "-u", str(users), 
        "-r", str(spawn_rate),
        "--host", "http://api-gateway:8000",
        "--csv", "/tmp/locust_report"
    ]
    
    locust_process = subprocess.Popen(
        cmd, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT, 
        text=True,
        bufsize=1,
        universal_newlines=True
    )
    return {"status": "success", "message": "Load test started"}

@app.get("/loadtest/results")
async def get_results():
    csv_path = "/tmp/locust_report_stats.csv"
    if os.path.exists(csv_path):
        return FileResponse(csv_path, filename="load_test_results.csv", media_type="text/csv")
    return {"status": "error", "message": "No results found. Run a load test first."}

@app.post("/loadtest/stop")
async def stop_loadtest():
    global locust_process
    if locust_process:
        locust_process.terminate()
        locust_process = None
        return {"status": "success", "message": "Load test stopped"}
    return {"status": "error", "message": "No load test running"}

@app.get("/loadtest/stats")
async def get_stats():
    import csv
    csv_path = "/tmp/locust_report_stats.csv"
    if os.path.exists(csv_path):
        try:
            with open(csv_path, 'r') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                if rows:
                    # Look for the 'Aggregated' row or the last line
                    stats = rows[-1]
                    return {
                        "rps": float(stats.get("Requests/s", 0)),
                        "latency": float(stats.get("Average Response Time", 0)),
                        "failures": float(stats.get("Failures/s", 0)),
                        "total_requests": int(stats.get("Request Count", 0))
                    }
        except Exception as e:
            return {"error": str(e)}
    return {"rps": 0, "latency": 0, "failures": 0, "total_requests": 0}

@app.websocket("/ws/logs/{service_name}")
async def stream_logs(websocket: WebSocket, service_name: str):
    await websocket.accept()
    try:
        if service_name == "load-test":
            global locust_process
            if locust_process:
                loop = asyncio.get_event_loop()
                while locust_process and locust_process.poll() is None:
                    # Non-blocking readline
                    line = await loop.run_in_executor(None, locust_process.stdout.readline)
                    if line:
                        await websocket.send_text(line)
                    else:
                        await asyncio.sleep(0.1)
            else:
                await websocket.send_text("Load test not running")
        else:
            try:
                container = client.containers.get(service_name)
                # Stream logs in a non-blocking way
                def get_logs():
                    return container.logs(stream=True, tail=100, follow=True)
                
                loop = asyncio.get_event_loop()
                log_stream = await loop.run_in_executor(None, lambda: container.logs(stream=True, tail=100, follow=True))
                
                await websocket.send_text(f"--- Connected to {service_name} log stream ---")
                
                while True:
                    # Get next line in a thread-safe/non-blocking way
                    try:
                        line = await loop.run_in_executor(None, lambda: next(log_stream, None))
                        if line is None:
                            break
                        await websocket.send_text(line.decode('utf-8'))
                    except StopIteration:
                        break
                    # Small sleep to ensure responsiveness
                    await asyncio.sleep(0.01)
            except Exception as e:
                await websocket.send_text(f"Error: {str(e)}")
    except WebSocketDisconnect:
        pass
