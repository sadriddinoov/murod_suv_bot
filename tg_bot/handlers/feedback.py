import os

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from tg_bot.keyboards.reply import home_keyboard, feedback_keyboard
from tg_bot.services.users import get_user_by_telegram_id
from tg_bot.services.feedback import create_feedback
from tg_bot.states.help_feedback import FeedbackState

router = Router()

ADMIN_IDS = [int(x.strip()) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]


@router.message(F.text.in_(["✍️ Fikr qoldirish", "✍️ Оставить отзыв"]))
async def feedback_start_handler(message: Message, state: FSMContext):
    await state.set_state(FeedbackState.waiting_for_rating)

    user = await get_user_by_telegram_id(message.from_user.id)
    lang = user.language if user else "uz"

    text = (
        "Montellani tanlaganingiz uchun rahmat.\n"
        "Agar siz bizning xizmatlarimiz sifatini yaxshilashga yordam bersangiz xursand bo'lardik.\n"
        "Buning uchun 5 ballik tizim asosida baholang"
        if lang == "uz"
        else
        "Спасибо, что выбрали нас.\n"
        "Нам будет приятно, если вы поможете улучшить качество сервиса.\n"
        "Пожалуйста, оцените нас по 5-балльной системе."
    )

    await message.answer(text, reply_markup=feedback_keyboard(lang))


@router.message(FeedbackState.waiting_for_rating, F.text.in_([
    "Hammasi yoqdi ❤️",
    "Yaxshi ⭐⭐⭐⭐⭐",
    "Yoqmadi ⭐⭐⭐",
    "Yomon ⭐⭐",
    "Juda yomon 👎🏻",
    "Очень понравилось ❤️",
    "Хорошо ⭐⭐⭐⭐⭐",
    "Не понравилось ⭐⭐⭐",
    "Плохо ⭐⭐",
    "Очень плохо 👎🏻",
]))
async def feedback_rating_handler(message: Message, state: FSMContext):
    user = await get_user_by_telegram_id(message.from_user.id)
    lang = user.language if user else "uz"

    mapping = {
        "Hammasi yoqdi ❤️": "5",
        "Yaxshi ⭐⭐⭐⭐⭐": "4",
        "Yoqmadi ⭐⭐⭐": "3",
        "Yomon ⭐⭐": "2",
        "Juda yomon 👎🏻": "1",
        "Очень понравилось ❤️": "5",
        "Хорошо ⭐⭐⭐⭐⭐": "4",
        "Не понравилось ⭐⭐⭐": "3",
        "Плохо ⭐⭐": "2",
        "Очень плохо 👎🏻": "1",
    }

    await state.update_data(selected_rating=mapping[message.text])

    text = (
        "O'z fikr va mulohazalaringizni qoldiring, biz ularni albatta ko'rib chiqamiz"
        if lang == "uz"
        else "Оставьте ваш комментарий, мы обязательно его рассмотрим"
    )

    await message.answer(text, reply_markup=ReplyKeyboardRemove())
    await state.set_state(FeedbackState.waiting_for_comment)


@router.message(FeedbackState.waiting_for_comment, F.text)
async def feedback_comment_handler(message: Message, state: FSMContext):
    user = await get_user_by_telegram_id(message.from_user.id)
    lang = user.language if user else "uz"

    data = await state.get_data()
    rating = data.get("selected_rating")

    if not rating:
        text = "Avval bahoni tanlang." if lang == "uz" else "Сначала выберите оценку."
        await message.answer(text, reply_markup=home_keyboard(lang))
        await state.clear()
        return

    comment = message.text.strip()

    if not comment:
        text = (
            "❌ Iltimos, fikr yoki izoh yozing."
            if lang == "uz"
            else "❌ Пожалуйста, напишите комментарий."
        )
        await message.answer(text)
        return

    await create_feedback(message.from_user.id, rating, comment)

    rating_display = {
        "5": "⭐⭐⭐⭐⭐",
        "4": "⭐⭐⭐⭐",
        "3": "⭐⭐⭐",
        "2": "⭐⭐",
     "1": "⭐",
    }.get(rating, rating)

    admin_text = (
        f"✍️ Yangi feedback\n\n"
        f"👤 Ism: {user.full_name if user else message.from_user.full_name}\n"
        f"📞 Telefon: {user.phone if user else '-'}\n"
        f"🆔 Telegram ID: {message.from_user.id}\n"
        f"⭐ Baho: {rating_display}\n"
        f"💬 Izoh: {comment}"
    )

    for admin_id in ADMIN_IDS:
        try:
            await message.bot.send_message(admin_id, admin_text)
        except Exception:
            pass

    text = (
        "✅ Fikringiz uchun rahmat.\n\n💧 Siz bosh menyudasiz.\nIltimos, kerakli bo'limni tanlang ⬇️"
        if lang == "uz"
        else
        "✅ Спасибо за отзыв.\n\n💧 Вы в главном меню.\nПожалуйста, выберите нужный раздел ⬇️"
    )

    await message.answer(text, reply_markup=home_keyboard(lang))
    await state.clear()


@router.message(FeedbackState.waiting_for_rating, F.text.in_(["⬅️ Orqaga", "⬅️ Назад"]))
async def feedback_back_handler(message: Message, state: FSMContext):
    user = await get_user_by_telegram_id(message.from_user.id)
    lang = user.language if user else "uz"

    text = (
        "💧 Siz bosh menyudasiz.\nIltimos, kerakli bo'limni tanlang ⬇️"
        if lang == "uz"
        else "💧 Вы в главном меню.\nПожалуйста, выберите нужный раздел ⬇️"
    )

    await message.answer(text, reply_markup=home_keyboard(lang))
    await state.clear()  