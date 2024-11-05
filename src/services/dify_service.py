# src/services/dify_service.py
import aiohttp
from typing import Dict, Optional
from ..config.settings import settings

class DifyService:
    def __init__(self):
        self.base_url = settings.DIFY_BASE_URL
        self.api_key = settings.DIFY_API_KEY

    def get_headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def chat_with_customer(self, 
                               message: str, 
                               conversation_id: Optional[str] = None,
                               customer_info: Optional[Dict] = None):
        url = f"{self.base_url}/chat-messages"
        
        # Thêm thông tin khách hàng vào context
        inputs = {}
        if customer_info:
            inputs["customer_info"] = customer_info
            
        data = {
            "inputs": inputs,
            "query": message,
            "response_mode": "streaming",
            "conversation_id": conversation_id,
            "user": customer_info.get("id") if customer_info else None
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=self.get_headers(), json=data) as response:
                return await response.json()

    async def create_order_from_chat(self, conversation_id: str, order_details: Dict):
        url = f"{self.base_url}/completion"
        data = {
            "inputs": {
                "order_details": order_details
            },
            "conversation_id": conversation_id
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=self.get_headers(), json=data) as response:
                return await response.json()

    async def initialize_conversation(self, customer_info: Dict):
        url = f"{self.base_url}/chat-messages"
        data = {
            "app_id": settings.DIFY_APP_ID,
            "user": customer_info.get("id"),
            "inputs": {
                "customer_name": customer_info.get("name"),
                "customer_history": customer_info.get("order_history")
            }
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=self.get_headers(), json=data) as response:
                return await response.json()

    async def process_order_intent(self, conversation_id: str, message_content: Dict):
        url = f"{self.base_url}/chat-messages/{conversation_id}/process-order"
        data = {
            "app_id": settings.DIFY_APP_ID,
            "message": message_content,
            "action": "create_order"
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=self.get_headers(), json=data) as response:
                return await response.json()

    async def process_streaming_response(self, response):
        result = ""
        async for chunk in response.content:
            if chunk:
                chunk_data = chunk.decode()
                result += chunk_data
                # Có thể xử lý từng chunk ở đây nếu cần
        return result