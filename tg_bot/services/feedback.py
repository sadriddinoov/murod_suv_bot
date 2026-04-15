from asgiref.sync import sync_to_async
from apps.users.models import TelegramUser
from apps.store.models import Feedback, HelpMessage


@sync_to_async
def create_feedback(telegram_id: int, rating: str, comment: str):
    user = TelegramUser.objects.filter(telegram_id=telegram_id).first()
    if not user:
        return None

    return Feedback.objects.create(
        user=user,
        rating=rating,
        comment=comment,
    )


@sync_to_async
def create_help_message(telegram_id: int, text: str):
    user = TelegramUser.objects.filter(telegram_id=telegram_id).first()
    if not user:
        return None

    return HelpMessage.objects.create(user=user, text=text)