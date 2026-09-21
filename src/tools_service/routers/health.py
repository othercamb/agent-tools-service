from fastapi import APIRouter

from tools_service.config import get_settings

router = APIRouter(tags=["health"])


@router.get("/health")
async def health() -> dict:
    return {"status": "ok", "app": get_settings().app_name}
