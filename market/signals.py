from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Order, CartItem, Favorite, Profile
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .telegram_bot import send_telegram_notification

@receiver(post_save, sender=Order)
def order_created(sender, instance, created, **kwargs):
    if created:
        # Send Telegram Notification
        send_telegram_notification(instance)

        # Send WebSocket Notification (existing logic)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'admin_orders',
            {
                'type': 'order_message',
                'message': 'Yangi buyurtma tushdi!',
                'order': {
                    'id': instance.id,
                    'full_name': instance.full_name,
                    'total_amount': float(instance.total_amount),
                    'created_at': instance.created_at.strftime("%d.%m.%Y %H:%M")
                }
            }
        )

@receiver(user_logged_in)
def merge_guest_cart(sender, request, user, **kwargs):
    guest_uuid = request.COOKIES.get('guest_uuid')
    if guest_uuid:
        # Merge Cart Items
        guest_items = CartItem.objects.filter(guest_uuid=guest_uuid)
        for item in guest_items:
            existing_item = CartItem.objects.filter(user=user, product=item.product).first()
            if existing_item:
                existing_item.quantity += item.quantity
                existing_item.save()
                item.delete()
            else:
                item.user = user
                item.guest_uuid = None
                item.save()
        
        # Merge Favorites
        guest_favorites = Favorite.objects.filter(guest_uuid=guest_uuid)
        for fav in guest_favorites:
            if not Favorite.objects.filter(user=user, product=fav.product).exists():
                fav.user = user
                fav.guest_uuid = None
                fav.save()
            else:
                fav.delete()

@receiver(post_save, sender=User)
@receiver(post_save, sender=Profile)
def broadcast_user_update(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'admin_orders', # Reusing same group for simplicity or can create 'admin_updates'
        {
            'type': 'user_update_message',
            'message': 'Mijozlar ro\'yxati yangilandi',
        }
    )

