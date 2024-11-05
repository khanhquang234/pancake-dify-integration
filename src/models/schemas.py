from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from datetime import datetime

class MessageData(BaseModel):
    """Schema cho dữ liệu tin nhắn"""
    text: str
    type: str = Field(default="text")
    attachments: Optional[List[Dict]] = None
    timestamp: datetime = Field(default_factory=datetime.now)

class SenderData(BaseModel):
    """Schema cho thông tin người gửi"""
    id: str
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

class PageData(BaseModel):
    """Schema cho thông tin page"""
    id: str
    name: Optional[str] = None
    platform: str = "facebook"

class WebhookData(BaseModel):
    """Schema chính cho webhook data"""
    event: str = Field(..., description="Loại sự kiện webhook")
    message: Optional[MessageData] = None
    sender: Optional[SenderData] = None
    page_id: str
    timestamp: int
    shop_id: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "event": "message",
                "message": {
                    "text": "Xin chào shop",
                    "type": "text"
                },
                "sender": {
                    "id": "123456789",
                    "name": "Khách hàng A"
                },
                "page_id": "987654321",
                "timestamp": 1634567890
            }
        }

class MessageResponse(BaseModel):
    text: str
    type: str = "text"
    page_id: str
    customer_id: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "Cảm ơn bạn đã liên hệ",
                "type": "text",
                "page_id": "123456789",
                "customer_id": "987654321"
            }
        }