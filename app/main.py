import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, BotCommand
from aiogram.fsm.context import FSMContext

from app.config import BOT_TOKEN
from app.keyboards import language_keyboard, phone_keyboard, home_keyboard
from app.states import StartState
from app.db import init_db, get_user_by_telegram_id, create_user


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Перезапуск бота"),
        BotCommand(command="menu", description="Меню"),
        BotCommand(command="cart", description="Корзина"),
        BotCommand(command="settings", description="Настройки"),
        BotCommand(command="help", description="Помощь"),
    ]
    await bot.set_my_commands(commands)


@dp.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    user = await get_user_by_telegram_id(message.from_user.id)

    if user:
        if user.language == "ru":
            text = "Выберите нужный раздел из главного меню."
        else:
            text = "Asosiy menyudan kerakli bo'limni tanlang."

        await state.clear()
        await message.answer(text, reply_markup=home_keyboard(user.language))
        return

    await state.set_state(StartState.choosing_language)
    await message.answer(
        "Tilni tanlang / Выберите язык",
        reply_markup=language_keyboard()
    )


@dp.message(
    StartState.choosing_language,
    F.text.in_(["🇺🇿 O'zbekcha", "🇷🇺 Русский"])
)
async def choose_language_handler(message: Message, state: FSMContext):
    lang = "uz" if message.text == "🇺🇿 O'zbekcha" else "ru"

    await state.update_data(lang=lang)
    await state.set_state(StartState.waiting_for_phone)

    if lang == "uz":
        text = "Iltimos, telefon raqamingizni yuboring"
    else:
        text = "Пожалуйста, отправьте ваш номер телефона"

    await message.answer(text, reply_markup=phone_keyboard(lang))


@dp.message(StartState.choosing_language)
async def invalid_language_handler(message: Message):
    await message.answer(
        "Tilni tugma orqali tanlang / Выберите язык кнопкой",
        reply_markup=language_keyboard()
    )


@dp.message(StartState.waiting_for_phone, F.contact)
async def get_phone_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "uz")
    phone = message.contact.phone_number
    full_name = message.from_user.full_name
    telegram_id = message.from_user.id

    existing_user = await get_user_by_telegram_id(telegram_id)
    if not existing_user:
        await create_user(
            telegram_id=telegram_id,
            full_name=full_name,
            phone=phone,
            language=lang,
        )

    if lang == "uz":
        text = "Rahmat, ro'yxatdan o'tdingiz.\n\nAsosiy menyudan kerakli bo'limni tanlang."
    else:
        text = "Спасибо, вы успешно зарегистрированы.\n\nВыберите нужный раздел из главного меню."

    await message.answer(text, reply_markup=home_keyboard(lang))
    await state.clear()


@dp.message(StartState.waiting_for_phone)
async def invalid_phone_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "uz")

    if lang == "uz":
        text = "Iltimos, telefon raqamingizni pastdagi tugma orqali yuboring."
    else:
        text = "Пожалуйста, отправьте номер телефона кнопкой ниже."

    await message.answer(text, reply_markup=phone_keyboard(lang))


@dp.message(Command("menu"))
async def menu_command_handler(message: Message):
    user = await get_user_by_telegram_id(message.from_user.id)
    lang = user.language if user else "uz"

    if lang == "ru":
        text = "Выберите нужный раздел из главного меню."
    else:
        text = "Asosiy menyudan kerakli bo'limni tanlang."

    await message.answer(text, reply_markup=home_keyboard(lang))


@dp.message(Command("cart"))
async def cart_command_handler(message: Message):
    user = await get_user_by_telegram_id(message.from_user.id)
    lang = user.language if user else "uz"

    if lang == "ru":
        await message.answer("Корзина пока пустая.")
    else:
        await message.answer("Savatcha hozircha bo'sh.")


@dp.message(Command("settings"))
async def settings_command_handler(message: Message):
    user = await get_user_by_telegram_id(message.from_user.id)
    lang = user.language if user else "uz"

    if lang == "ru":
        await message.answer("Раздел настроек пока в разработке.")
    else:
        await message.answer("Sozlamalar bo'limi hozircha ishlab chiqilmoqda.")


@dp.message(Command("help"))
async def help_command_handler(message: Message):
    user = await get_user_by_telegram_id(message.from_user.id)
    lang = user.language if user else "uz"

    if lang == "ru":
        await message.answer("Раздел помощи пока в разработке.")
    else:
        await message.answer("Yordam bo'limi hozircha ishlab chiqilmoqda.")


@dp.message(F.text.in_(["💧 Mahsulotlar", "💧 Товары"]))
async def products_handler(message: Message):
    if message.text == "💧 Mahsulotlar":
        await message.answer("Bu yerda keyingi stepda mahsulotlar chiqadi.")
    else:
        await message.answer("Здесь на следующем шаге будут товары.")


@dp.message(F.text.in_(["🛒 Savatcha", "🛒 Корзина"]))
async def cart_handler(message: Message):
    if message.text == "🛒 Savatcha":
        await message.answer("Savatcha hozircha bo'sh.")
    else:
        await message.answer("Корзина пока пустая.")


@dp.message(F.text.in_(["✍️ Fikr qoldirish", "✍️ Оставить отзыв"]))
async def feedback_handler(message: Message):
    if message.text == "✍️ Fikr qoldirish":
        await message.answer("Bu bo'lim keyingi stepda qilinadi.")
    else:
        await message.answer("Этот раздел сделаем позже.")


@dp.message(F.text.in_(["🔎 Yordam", "🔎 Помощь"]))
async def help_handler(message: Message):
    if message.text == "🔎 Yordam":
        await message.answer("Yordam bo'limi keyingi stepda to'ldiriladi.")
    else:
        await message.answer("Раздел помощи заполним позже.")


@dp.message(F.text.in_(["🛠 Sozlamalar", "🛠 Настройки"]))
async def settings_handler(message: Message):
    if message.text == "🛠 Sozlamalar":
        await message.answer("Sozlamalar bo'limi keyingi stepda qilinadi.")
    else:
        await message.answer("Раздел настроек сделаем позже.")


async def main():
    await init_db()
    await set_bot_commands(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())