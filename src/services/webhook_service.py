# src/services/webhook_service.py
from typing import Dict
from .dify_service import DifyService
from .pancake_service import PancakeService

class WebhookService:
    def __init__(self):
        self.dify = DifyService()
        self.pancake = PancakeService()

    async def handle_pancake_message(self, webhook_data: Dict):
        message = webhook_data.get("message", {}).get("text")
        customer_id = webhook_data.get("sender", {}).get("id")
        page_id = webhook_data.get("page_id")
        
        # Lấy thông tin khách hàng và lịch sử đơn hàng
        customer_info = self.pancake.get_customer_info(customer_id)
        customer_orders = self.pancake.get_customer_orders(customer_id)
        
        # Tổng hợp context cho Dify
        context = {
            "customer": customer_info,
            "order_history": customer_orders
        }
        
        # Xử lý với Dify
        dify_response = await self.dify.chat_with_customer(
            message=message,
            conversation_id=customer_id,
            customer_info=context
        )
        
        # Gửi phản hồi từ Dify về Pancake
        ai_message = dify_response.get("answer", "")
        if ai_message:
            self.pancake.send_message_to_customer(
                page_id=page_id,
                customer_id=customer_id,
                message=ai_message
            )
        
        # Xử lý đặt hàng nếu có
        if self._detect_order_intent(dify_response):
            order_details = self._extract_order_details(dify_response)
            order = self.pancake.create_order(order_details)
            
        return dify_response

    def _detect_order_intent(self, dify_response: Dict) -> bool:
        # Kiểm tra response từ Dify có chứa ý định đặt hàng không
        answer = dify_response.get("answer", "").lower()
        order_keywords = ["đặt hàng", "mua", "order", "thanh toán", "giỏ hàng"]
        return any(keyword in answer for keyword in order_keywords)

    def _extract_order_details(self, dify_response: Dict) -> Dict:
        # Trích xuất thông tin đơn hàng từ response của Dify
        return {
            "items": dify_response.get("order_items", []),
            "customer_info": dify_response.get("customer_info", {}),
            "shipping_address": dify_response.get("shipping_address", {}),
            "payment_method": dify_response.get("payment_method", "COD")
        }