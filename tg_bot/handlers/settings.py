from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from tg_bot.keyboards.reply import home_keyboard, settings_keyboard, change_language_keyboard
from tg_bot.services.users import get_user_by_telegram_id, update_user_language
from tg_bot.states.settings import SettingsState

router = Router()


@router.message(F.text.in_(["⚙️ Sozlamalar", "⚙️ Настройки"]))
async def settings_handler(message: Message, state: FSMContext):
    await state.clear()

    user = await get_user_by_telegram_id(message.from_user.id)
    lang = user.language if user else "uz"

    text = "⚙️ Sozlamalar bo'limi" if lang == "uz" else "⚙️ Раздел настроек"

    await message.answer(text, reply_markup=settings_keyboard(lang))


@router.message(F.text.in_(["🌐 Tilni o'zgartirish", "🌐 Сменить язык"]))
async def change_language_handler(message: Message, state: FSMContext):
    await state.set_state(SettingsState.waiting_for_language_choice)
    await message.answer(
        "🌐 Tilni tanlang / Выберите язык",
        reply_markup=change_language_keyboard()
    )


@router.message(SettingsState.waiting_for_language_choice, F.text.in_(["🇺🇿 O'zbekcha", "🇷🇺 Русский"]))
async def save_new_language_handler(message: Message, state: FSMContext):
    new_lang = "uz" if message.text == "🇺🇿 O'zbekcha" else "ru"

    await update_user_language(message.from_user.id, new_lang)

    text = (
        "✅ Til muvaffaqiyatli o'zgartirildi.\n\n💧 Siz bosh menyudasiz.\nIltimos, kerakli bo'limni tanlang ⬇️"
        if new_lang == "uz"
        else "✅ Язык успешно изменён.\n\n💧 Вы в главном меню.\nПожалуйста, выберите нужный раздел ⬇️"
    )

    await message.answer(text, reply_markup=home_keyboard(new_lang))
    await state.clear()


@router.message(SettingsState.waiting_for_language_choice)
async def invalid_language_choice_handler(message: Message):
    await message.answer(
        "🌐 Tilni tugma orqali tanlang / Выберите язык кнопкой",
        reply_markup=change_language_keyboard()
    )