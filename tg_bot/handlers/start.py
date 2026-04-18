from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import BotCommand, Message

from tg_bot.keyboards.reply import home_keyboard, language_keyboard, phone_keyboard
from tg_bot.services.users import create_or_update_user, get_user_by_telegram_id
from tg_bot.states.start import StartState

router = Router()


async def set_bot_commands(bot):
    ru_commands = [
        BotCommand(command="start", description="🔄 Перезапуск бота"),
        BotCommand(command="menu", description="🏠 Главное меню"),
        BotCommand(command="cart", description="🛒 Корзина"),
        BotCommand(command="settings", description="⚙️ Настройки"),
        BotCommand(command="help", description="📞 Помощь"),
    ]

    uz_commands = [
        BotCommand(command="start", description="🔄 Botni qayta ishga tushirish"),
        BotCommand(command="menu", description="🏠 Asosiy menyu"),
        BotCommand(command="cart", description="🛒 Savatcha"),
        BotCommand(command="settings", description="⚙️ Sozlamalar"),
        BotCommand(command="help", description="📞 Yordam"),
    ]

    await bot.set_my_commands(uz_commands)
    await bot.set_my_commands(ru_commands, language_code="ru")
    await bot.set_my_commands(uz_commands, language_code="uz")


@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    user = await get_user_by_telegram_id(message.from_user.id)

    if user:
        text = (
            "💧 Siz bosh menyudasiz.\nIltimos, kerakli bo'limni tanlang ⬇️"
            if user.language == "uz"
            else "💧 Вы в главном меню.\nПожалуйста, выберите нужный раздел ⬇️"
        )
        await state.clear()
        await message.answer(text, reply_markup=home_keyboard(user.language))
        return

    await state.set_state(StartState.choosing_language)
    await message.answer(
        "🌐 Tilni tanlang / Выберите язык",
        reply_markup=language_keyboard(),
    )


@router.message(Command("menu"))
async def menu_command_handler(message: Message):
    user = await get_user_by_telegram_id(message.from_user.id)
    lang = user.language if user else "uz"

    text = (
        "💧 Siz bosh menyudasiz.\nIltimos, kerakli bo'limni tanlang ⬇️"
        if lang == "uz"
        else "💧 Вы в главном меню.\nПожалуйста, выберите нужный раздел ⬇️"
    )
    await message.answer(text, reply_markup=home_keyboard(lang))


@router.message(Command("lang"))
async def lang_command_handler(message: Message):
    await message.answer(f"🌐 language_code: {message.from_user.language_code}")


@router.message(StartState.choosing_language, F.text.in_(["🇺🇿 O'zbekcha", "🇷🇺 Русский"]))
async def choose_language_handler(message: Message, state: FSMContext):
    lang = "uz" if message.text == "🇺🇿 O'zbekcha" else "ru"
    await state.update_data(lang=lang)
    await state.set_state(StartState.waiting_for_phone)

    text = (
        "📱 Iltimos, telefon raqamingizni yuboring"
        if lang == "uz"
        else "📱 Пожалуйста, отправьте ваш номер телефона"
    )
    await message.answer(text, reply_markup=phone_keyboard(lang))


@router.message(StartState.choosing_language)
async def invalid_language_handler(message: Message):
    await message.answer(
        "🌐 Tilni tugma orqali tanlang / Выберите язык кнопкой",
        reply_markup=language_keyboard(),
    )


@router.message(StartState.waiting_for_phone, F.contact)
async def get_phone_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "uz")

    await create_or_update_user(
        telegram_id=message.from_user.id,
        full_name=message.from_user.full_name,
        phone=message.contact.phone_number,
        language=lang,
    )

    text = (
        "✅ Rahmat, siz muvaffaqiyatli ro'yxatdan o'tdingiz.\n\n💧 Siz bosh menyudasiz.\nIltimos, kerakli bo'limni tanlang ⬇️"
        if lang == "uz"
        else "✅ Спасибо, вы успешно зарегистрированы.\n\n💧 Вы в главном меню.\nПожалуйста, выберите нужный раздел ⬇️"
    )
    await message.answer(text, reply_markup=home_keyboard(lang))
    await state.clear()


@router.message(StartState.waiting_for_phone)
async def invalid_phone_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "uz")

    text = (
        "📱 Iltimos, telefon raqamingizni pastdagi tugma orqali yuboring."
        if lang == "uz"
        else "📱 Пожалуйста, отправьте номер телефона кнопкой ниже."
    )
    await message.answer(text, reply_markup=phone_keyboard(lang))
