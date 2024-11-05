# src/api/routes.py
from fastapi import APIRouter, HTTPException, Header
from typing import Optional
from ..services.webhook_service import WebhookService
from ..models.schemas import WebhookData
from ..utils.auth import verify_pancake_webhook

router = APIRouter()
webhook_service = WebhookService()

@router.post("/webhook/pancake")
async def pancake_webhook(
    data: WebhookData,
    x_pancake_signature: Optional[str] = Header(None)
):
    # Verify webhook signature
    if not verify_pancake_webhook(data.dict(), x_pancake_signature):
        raise HTTPException(status_code=401, detail="Invalid webhook signature")
        
    try:
        response = await webhook_service.handle_pancake_message(data.dict())
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))