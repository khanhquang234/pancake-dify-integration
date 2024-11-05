# src/services/pancake_service.py
import requests
from typing import Dict, List
from ..config.settings import settings

class PancakeService:
    def __init__(self):
        self.base_url = settings.PANCAKE_BASE_URL
        self.api_key = settings.PANCAKE_API_KEY
        self.shop_id = settings.PANCAKE_SHOP_ID

    def get_headers(self):
        return {
            "Content-Type": "application/json"
        }
        
    def get_customer_info(self, customer_id: str):
        url = f"{self.base_url}/shops/{self.shop_id}/customers/{customer_id}?api_key={self.api_key}"
        response = requests.get(url, headers=self.get_headers())
        return response.json()

    def create_order(self, order_data: Dict):
        url = f"{self.base_url}/shops/{self.shop_id}/orders?api_key={self.api_key}"
        response = requests.post(url, headers=self.get_headers(), json=order_data)
        return response.json()
        
    def get_product_inventory(self, warehouse_id: str):
        url = f"{self.base_url}/shops/{self.shop_id}/variations_warehouses?api_key={self.api_key}&warehouse_id={warehouse_id}"
        response = requests.get(url, headers=self.get_headers())
        return response.json()

    def get_customer_orders(self, customer_id: str):
        url = f"{self.base_url}/shops/{self.shop_id}/orders?api_key={self.api_key}&customer_id={customer_id}"
        response = requests.get(url, headers=self.get_headers())
        return response.json()

    def handle_message(self, page_id: str, message: str, customer_id: str):
        url = f"{self.base_url}/shops/{self.shop_id}/messages?api_key={self.api_key}"
        data = {
            "page_id": page_id,
            "customer_id": customer_id,
            "message": message
        }
        response = requests.post(url, headers=self.get_headers(), json=data)
        return response.json()

    def setup_webhook(self):
        url = f"{self.base_url}/shops/{self.shop_id}?api_key={self.api_key}"
        webhook_config = {
            "webhook_enable": True,
            "webhook_url": "your_webhook_url",
            "webhook_types": ["messages", "orders", "customers"],
            "webhook_headers": {
                "X-API-KEY": settings.PANCAKE_WEBHOOK_SECRET
            }
        }
        response = requests.put(url, headers=self.get_headers(), json={"shop": webhook_config})
        return response.json()

    def send_message_to_customer(self, page_id: str, customer_id: str, message: str):
        url = f"{self.base_url}/shops/{self.shop_id}/messages?api_key={self.api_key}"
        data = {
            "page_id": page_id,
            "customer_id": customer_id,
            "message": {
                "text": message,
                "type": "text"
            }
        }
        response = requests.post(url, headers=self.get_headers(), json=data)
        return response.json()