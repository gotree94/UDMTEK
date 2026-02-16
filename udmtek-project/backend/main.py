"""
UDMTEK Backend Main Application
FastAPI-based REST API server for PLC translation and analysis
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
from typing import List

from api.routes import plc_parser, udml_translator, ai_analysis, dashboard
from infrastructure.data_collection.realtime_collector import RealtimeCollector
from infrastructure.storage.database import init_db, close_db

# Application lifespan management
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting UDMTEK Backend...")
    await init_db()
    print("✅ Database initialized")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down UDMTEK Backend...")
    await close_db()
    print("✅ Database closed")

# Initialize FastAPI application
app = FastAPI(
    title="UDMTEK API",
    description="World's First PLC Translation Technology - AI-powered Industrial Automation Analysis",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(plc_parser.router, prefix="/api/v1/parser", tags=["PLC Parser"])
app.include_router(udml_translator.router, prefix="/api/v1/udml", tags=["UDML Translator"])
app.include_router(ai_analysis.router, prefix="/api/v1/ai", tags=["AI Analysis"])
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["Dashboard"])

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

# WebSocket endpoint for real-time data
@app.websocket("/ws/realtime")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            # Echo back for now (implement real-time data streaming)
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "UDMTEK API Server",
        "version": "1.0.0",
        "description": "World's First PLC Translation Technology",
        "docs": "/docs",
        "redoc": "/redoc"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "UDMTEK Backend",
        "version": "1.0.0"
    }

# Main entry point
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
