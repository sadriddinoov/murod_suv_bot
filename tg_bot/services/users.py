from asgiref.sync import sync_to_async
from apps.users.models import TelegramUser


@sync_to_async
def get_user_by_telegram_id(telegram_id: int):
    return TelegramUser.objects.filter(telegram_id=telegram_id).first()


@sync_to_async
def create_or_update_user(telegram_id: int, full_name: str, phone: str, language: str):
    user, _ = TelegramUser.objects.update_or_create(
        telegram_id=telegram_id,
        defaults={
            "full_name": full_name,
            "phone": phone,
            "language": language,
        },
    )
    return user


from asgiref.sync import sync_to_async
from apps.users.models import TelegramUser


@sync_to_async
def update_user_language(telegram_id: int, language: str):
    user = TelegramUser.objects.filter(telegram_id=telegram_id).first()
    if not user:
        return None

    user.language = language
    user.save(update_fields=["language"])
    return user