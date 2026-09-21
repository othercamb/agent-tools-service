from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("/post-call")
async def post_call() -> dict:
    """Day 5:
    1. read the raw body (request.body()) and the X-Signature header
    2. reject with 401 if security.verify_signature fails
    3. parse the body into models.PostCallEvent
    4. if event_id is already in processed_events, return {"duplicate": True}
    5. otherwise store it and return {"accepted": True}
    """
    raise HTTPException(status_code=501, detail="Day 5: not implemented yet")
