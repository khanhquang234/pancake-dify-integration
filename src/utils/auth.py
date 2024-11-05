import hmac
import hashlib
from ..config.settings import settings

def verify_pancake_webhook(payload: dict, signature: str) -> bool:
    """
    Xác thực webhook signature từ Pancake POS
    """
    if not signature:
        return False
        
    expected = hmac.new(
        settings.PANCAKE_WEBHOOK_SECRET.encode(),
        str(payload).encode(),
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(signature, expected)