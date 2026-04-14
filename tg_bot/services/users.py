from asgiref.sync import sync_to_async
from apps.users.models import TelegramUser


@sync_to_async
def get_user_by_telegram_id(telegram_id: int):
    try:
        return TelegramUser.objects.get(telegram_id=telegram_id)
    except TelegramUser.DoesNotExist:
        return None


@sync_to_async
def create_or_update_user(telegram_id: int, full_name: str, phone: str, language: str):
    user, _ = TelegramUser.objects.update_or_create(
        telegram_id=telegram_id,
        defaults={
            'full_name': full_name,
            'phone': phone,
            'language': language,
        }
    )
    return user
