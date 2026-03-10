import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_telegram_notification(order):
    """
    Sends a telegram notification about a new order to all configured chat IDs.
    """
    token = settings.TELEGRAM_BOT_TOKEN
    chat_ids = settings.TELEGRAM_CHAT_IDS

    if not token or not chat_ids:
        logger.warning("Telegram token or chat_ids are missing. Notification not sent.")
        return False

    message = (
        f"🆕 <b>Yangi buyurtma!</b>\n\n"
        f"🆔 <b>ID:</b> {order.id}\n"
        f"👤 <b>Mijoz:</b> {order.full_name}\n"
        f"📞 <b>Tel:</b> {order.phone_number}\n"
        f"💰 <b>Summa:</b> {order.total_amount:,.0f} so'm\n"
        f"📍 <b>Manzil:</b> {order.address}\n\n"
        f"📅 <b>Vaqt:</b> {order.created_at.strftime('%d.%m.%Y %H:%M')}"
    )

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    success = True
    for chat_id in chat_ids:
        if not chat_id.strip():
            continue
            
        payload = {
            'chat_id': chat_id.strip(),
            'text': message,
            'parse_mode': 'HTML'
        }

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
        except Exception as e:
            logger.error(f"Telegram notification error for chat_id {chat_id}: {e}")
            success = False
            
    return success
