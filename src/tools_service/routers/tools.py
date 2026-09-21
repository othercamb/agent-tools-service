from fastapi import APIRouter, HTTPException

from tools_service.models import OrderStatus

router = APIRouter(prefix="/tools", tags=["tools"])


@router.get("/order-status/{order_id}", response_model=OrderStatus)
async def order_status(order_id: str) -> OrderStatus:
    """Day 4: look the order up with db.fetch_order and return it.

    Return 404 when the order does not exist, so the agent can tell the user plainly.
    """
    raise HTTPException(status_code=501, detail="Day 4: not implemented yet")
