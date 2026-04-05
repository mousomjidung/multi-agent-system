"""
Entry point. Simple FastAPI server.
MCP runs via stdio subprocess — no port conflicts, no lifespan issues.
"""
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

PORT = int(os.environ.get("PORT", "8080"))
print(f"Starting on port {PORT}...", flush=True)

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI(title="Multi-Agent AI System", version="1.0.0")

from api.routes import router
app.include_router(router)

@app.get("/")
async def index():
    return FileResponse("frontend/index.html")

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    print(f"🚀 http://0.0.0.0:{PORT}", flush=True)
    uvicorn.run(app, host="0.0.0.0", port=PORT)
