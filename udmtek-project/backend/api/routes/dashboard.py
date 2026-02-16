"""Dashboard API Routes"""
from fastapi import APIRouter
router = APIRouter()

@router.get("/stats")
async def get_system_stats():
    return {
        "total_plcs": 12,
        "active_plcs": 10,
        "critical_alerts": 2,
        "pending_maintenance": 5,
        "avg_health_score": 78.5
    }

@router.get("/health-trend")
async def get_health_trend():
    return {"status": "ok", "data": []}
