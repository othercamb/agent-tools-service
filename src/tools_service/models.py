from typing import Literal

from pydantic import BaseModel, Field

OrderState = Literal["processing", "in_transit", "delivered", "cancelled"]


class OrderStatus(BaseModel):
    """What the agent receives when it calls the order-status tool."""

    order_id: str = Field(pattern=r"^ORD-\d{4}$")
    status: OrderState
    eta: str | None = None
    last_update: str


class PostCallEvent(BaseModel):
    """Day 5: payload sent by the agent platform when a conversation ends."""

    event_id: str
    conversation_id: str
    summary: str
    data: dict = Field(default_factory=dict)
