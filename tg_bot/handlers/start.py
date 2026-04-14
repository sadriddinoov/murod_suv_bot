from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, BotCommand
from aiogram.fsm.context import FSMContext

from tg_bot.states.start import StartState
from tg_bot.keyboards.reply import language_keyboard, phone_keyboard, home_keyboard
from tg_bot.services.users import get_user_by_telegram_id, create_or_update_user

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
            "Siz bosh menyudasiz.\nIltimos, kerakli bo'limni tanlang ⬇️"
            if user.language == "uz"
            else "Вы в главном меню.\nПожалуйста, выберите нужный раздел ⬇️"
        )
        await state.clear()
        await message.answer(text, reply_markup=home_keyboard(user.language))
        return

    await state.set_state(StartState.choosing_language)
    await message.answer(
        "🌐 Tilni tanlang / Выберите язык",
        reply_markup=language_keyboard()
    )


@router.message(Command("menu"))
async def menu_command_handler(message: Message):
    user = await get_user_by_telegram_id(message.from_user.id)
    lang = user.language if user else "uz"

    text = (
        "Siz bosh menyudasiz.\nIltimos, kerakli bo'limni tanlang ⬇️"
        if lang == "uz"
        else "Вы в главном меню.\nПожалуйста, выберите нужный раздел ⬇️"
    )
    await message.answer(text, reply_markup=home_keyboard(lang))


@router.message(Command("help"))
async def help_command_handler(message: Message):
    user = await get_user_by_telegram_id(message.from_user.id)
    lang = user.language if user else "uz"

    text = (
        "📞 Yordam bo'limi keyingi stepda to'ldiriladi."
        if lang == "uz"
        else "📞 Раздел помощи добавим на следующем этапе."
    )
    await message.answer(text)


@router.message(Command("cart"))
async def cart_command_handler(message: Message):
    user = await get_user_by_telegram_id(message.from_user.id)
    lang = user.language if user else "uz"

    text = (
        "🛒 Savatcha hozircha bo'sh."
        if lang == "uz"
        else "🛒 Корзина пока пустая."
    )
    await message.answer(text)


@router.message(Command("settings"))
async def settings_command_handler(message: Message):
    user = await get_user_by_telegram_id(message.from_user.id)
    lang = user.language if user else "uz"

    text = (
        "⚙️ Sozlamalar bo'limini keyingi stepda qilamiz."
        if lang == "uz"
        else "⚙️ Раздел настроек добавим на следующем этапе."
    )
    await message.answer(text)


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
        reply_markup=language_keyboard()
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
        "✅ Rahmat, siz muvaffaqiyatli ro'yxatdan o'tdingiz.\n\n Siz bosh menyudasiz.\nIltimos, kerakli bo'limni tanlang ⬇️"
        if lang == "uz"
        else "✅ Спасибо, вы успешно зарегистрированы.\n\n Вы в главном меню.\nПожалуйста, выберите нужный раздел ⬇️"
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


@router.message(F.text.in_(["💧 Mahsulotlar", "💧 Товары"]))
async def products_handler(message: Message):
    if message.text == "💧 Mahsulotlar":
        await message.answer("💧 Mahsulotlar bo'limini keyingi stepda ulaymiz.")
    else:
        await message.answer("💧 Раздел товаров подключим на следующем этапе.")


@router.message(F.text.in_(["🛒 Savatcha", "🛒 Корзина"]))
async def cart_handler(message: Message):
    if message.text == "🛒 Savatcha":
        await message.answer("🛒 Savatcha hozircha bo'sh.")
    else:
        await message.answer("🛒 Корзина пока пустая.")


@router.message(F.text.in_(["✍️ Fikr qoldirish", "✍️ Оставить отзыв"]))
async def feedback_handler(message: Message):
    if message.text == "✍️ Fikr qoldirish":
        await message.answer("✍️ Fikr qoldirish bo'limi keyingi stepda qilinadi.")
    else:
        await message.answer("✍️ Раздел отзывов добавим на следующем этапе.")


@router.message(F.text.in_(["📞 Yordam", "📞 Помощь"]))
async def help_menu_handler(message: Message):
    if message.text == "📞 Yordam":
        await message.answer("📞 Yordam bo'limi keyingi stepda to'ldiriladi.")
    else:
        await message.answer("📞 Раздел помощи заполним на следующем этапе.")


@router.message(F.text.in_(["⚙️ Sozlamalar", "⚙️ Настройки"]))
async def settings_handler(message: Message):
    if message.text == "⚙️ Sozlamalar":
        await message.answer("⚙️ Sozlamalar bo'limini keyingi stepda qilamiz.")
    else:
        await message.answer("⚙️ Раздел настроек добавим на следующем этапе.")