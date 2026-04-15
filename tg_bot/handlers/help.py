import os

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from tg_bot.keyboards.reply import home_keyboard, help_keyboard, cancel_keyboard
from tg_bot.services.users import get_user_by_telegram_id
from tg_bot.services.feedback import create_help_message
from tg_bot.states.help_feedback import HelpState

router = Router()

ADMIN_IDS = [int(x.strip()) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]
PHONE_NUMBER = os.getenv("SUPPORT_PHONE", "+998 78 777-1777")


@router.message(F.text.in_(["📞 Yordam", "📞 Помощь"]))
async def help_handler(message: Message, state: FSMContext):
    await state.clear()

    user = await get_user_by_telegram_id(message.from_user.id)
    lang = user.language if user else "uz"

    text = (
        "Buyruqlar:\n"
        "/start — Botni qaytadan ishga tushurish\n"
        "/menu — Menyu\n"
        "/cart — Savatcha\n"
        "/settings — Sozlamalar\n"
        "/help — Yordam\n\n"
        "Quyidan yordam turini tanlab, qisqacha ma'lumotga ega bo'lishingiz mumkin. Agar siz savollarga javob ololmasangiz operator bilan bog'laning."
        if lang == "uz"
        else
        "Команды:\n"
        "/start — Перезапуск бота\n"
        "/menu — Меню\n"
        "/cart — Корзина\n"
        "/settings — Настройки\n"
        "/help — Помощь\n\n"
        "Ниже выберите тип помощи. Если не найдете ответ, свяжитесь с оператором."
    )

    await message.answer(text, reply_markup=help_keyboard(lang))


@router.message(F.text.in_(["📞 Telefon orqali bog'lanish", "📞 Связаться по телефону"]))
async def help_phone_handler(message: Message):
    user = await get_user_by_telegram_id(message.from_user.id)
    lang = user.language if user else "uz"

    text = (
        f"Bizning raqam: {PHONE_NUMBER}"
        if lang == "uz"
        else f"Наш номер: {PHONE_NUMBER}"
    )
    await message.answer(text, reply_markup=help_keyboard(lang))


@router.message(F.text.in_(["📬 Xabar jo'natish", "📬 Отправить сообщение"]))
async def help_message_start_handler(message: Message, state: FSMContext):
    await state.set_state(HelpState.waiting_for_message)

    user = await get_user_by_telegram_id(message.from_user.id)
    lang = user.language if user else "uz"

    text = (
        "Bizga o'z xabaringizni jo'nating:"
        if lang == "uz"
        else "Отправьте нам ваше сообщение:"
    )
    await message.answer(text, reply_markup=cancel_keyboard(lang))


@router.message(HelpState.waiting_for_message, F.text.in_(["Bekor qilish", "Отмена"]))
async def cancel_help_message_handler(message: Message, state: FSMContext):
    user = await get_user_by_telegram_id(message.from_user.id)
    lang = user.language if user else "uz"

    text = (
        "💧 Siz bosh menyudasiz.\nIltimos, kerakli bo'limni tanlang ⬇️"
        if lang == "uz"
        else "💧 Вы в главном меню.\nПожалуйста, выберите нужный раздел ⬇️"
    )

    await message.answer(text, reply_markup=home_keyboard(lang))
    await state.clear()


@router.message(HelpState.waiting_for_message, F.text)
async def help_message_save_handler(message: Message, state: FSMContext):
    user = await get_user_by_telegram_id(message.from_user.id)
    lang = user.language if user else "uz"

    text_value = message.text.strip()
    if not text_value:
        text = (
            "❌ Xabar yozing."
            if lang == "uz"
            else "❌ Напишите сообщение."
        )
        await message.answer(text)
        return

    await create_help_message(message.from_user.id, text_value)

    admin_text = (
        f"📬 Yangi xabar\n\n"
        f"👤 Ism: {user.full_name if user else message.from_user.full_name}\n"
        f"📞 Telefon: {user.phone if user else '-'}\n"
        f"🆔 Telegram ID: {message.from_user.id}\n"
        f"💬 Xabar: {text_value}"
    )

    for admin_id in ADMIN_IDS:
        try:
            await message.bot.send_message(admin_id, admin_text)
        except Exception:
            pass

    text = (
        "✅ Xabaringiz yuborildi.\n\n💧 Siz bosh menyudasiz.\nIltimos, kerakli bo'limni tanlang ⬇️"
        if lang == "uz"
        else
        "✅ Ваше сообщение отправлено.\n\n💧 Вы в главном меню.\nПожалуйста, выберите нужный раздел ⬇️"
    )

    await message.answer(text, reply_markup=home_keyboard(lang))
    await state.clear()


@router.message(F.text.in_(["🛒 Buyurtma tarixi", "🛒 История заказов"]))
async def order_history_handler(message: Message):
    user = await get_user_by_telegram_id(message.from_user.id)
    lang = user.language if user else "uz"

    text = (
        "🛒 Buyurtma tarixi hozircha bo'sh."
        if lang == "uz"
        else "🛒 История заказов пока пуста."
    )
    await message.answer(text, reply_markup=help_keyboard(lang))


@router.message(F.text.in_(["⬅️ Orqaga", "⬅️ Назад"]))
async def help_back_handler(message: Message, state: FSMContext):
    user = await get_user_by_telegram_id(message.from_user.id)
    lang = user.language if user else "uz"

    text = (
        "💧 Siz bosh menyudasiz.\nIltimos, kerakli bo'limni tanlang ⬇️"
        if lang == "uz"
        else "💧 Вы в главном меню.\nПожалуйста, выберите нужный раздел ⬇️"
    )

    await message.answer(text, reply_markup=home_keyboard(lang))
    await state.clear()