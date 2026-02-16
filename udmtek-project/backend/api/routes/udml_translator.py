"""UDML Translator API Routes"""
from fastapi import APIRouter
router = APIRouter()

@router.post("/translate")
async def translate_to_udml(data: dict):
    return {"status": "not_implemented"}

@router.get("/complexity/{program_id}")
async def get_complexity(program_id: str):
    return {"program_id": program_id, "status": "not_implemented"}
