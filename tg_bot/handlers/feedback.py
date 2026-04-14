import os

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from tg_bot.keyboards.reply import home_keyboard
from tg_bot.services.users import get_user_by_telegram_id
from tg_bot.states.settings import FeedbackState

router = Router()

ADMIN_IDS = [
    int(x.strip())
    for x in os.getenv("ADMIN_IDS", "").split(",")
    if x.strip()
]


@router.message(F.text.in_(["✍️ Fikr qoldirish", "✍️ Оставить отзыв"]))
async def feedback_start_handler(message: Message, state: FSMContext):
    await state.set_state(FeedbackState.waiting_for_feedback)

    user = await get_user_by_telegram_id(message.from_user.id)
    lang = user.language if user else "uz"

    text = (
        "✍️ Fikringizni yozib qoldiring:"
        if lang == "uz"
        else "✍️ Напишите ваш отзыв:"
    )

    await message.answer(text)


@router.message(FeedbackState.waiting_for_feedback, F.text)
async def feedback_save_handler(message: Message, state: FSMContext):
    user = await get_user_by_telegram_id(message.from_user.id)
    lang = user.language if user else "uz"

    feedback_text = message.text

    admin_text = (
        f"✍️ Yangi fikr qoldirildi\n\n"
        f"👤 Ism: {user.full_name if user else message.from_user.full_name}\n"
        f"📞 Telefon: {user.phone if user else '-'}\n"
        f"🆔 Telegram ID: {message.from_user.id}\n"
        f"💬 Xabar:\n{feedback_text}"
    )

    for admin_id in ADMIN_IDS:
        try:
            await message.bot.send_message(chat_id=admin_id, text=admin_text)
        except Exception:
            pass

    text = (
        "✅ Fikringiz uchun rahmat.\n\n💧 Siz bosh menyudasiz.\nIltimos, kerakli bo'limni tanlang ⬇️"
        if lang == "uz"
        else "✅ Спасибо за отзыв.\n\n💧 Вы в главном меню.\nПожалуйста, выберите нужный раздел ⬇️"
    )

    await message.answer(text, reply_markup=home_keyboard(lang))
    await state.clear()