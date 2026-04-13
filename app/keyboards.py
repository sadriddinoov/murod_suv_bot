from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


def language_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🇺🇿 O'zbekcha")],
            [KeyboardButton(text="🇷🇺 Русский")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def phone_keyboard(lang: str) -> ReplyKeyboardMarkup:
    if lang == "uz":
        text = "📱 Raqamni yuborish"
    else:
        text = "📱 Поделиться номером"

    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=text, request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def home_keyboard(lang: str) -> ReplyKeyboardMarkup:
    if lang == "uz":
        keyboard = [
            [
                KeyboardButton(text="💧 Mahsulotlar"),
                KeyboardButton(text="🛒 Savatcha"),
            ],
            [
                KeyboardButton(text="✍️ Fikr qoldirish"),
                KeyboardButton(text="🔎 Yordam"),
            ],
            [
                KeyboardButton(text="🛠 Sozlamalar"),
            ],
        ]
    else:
        keyboard = [
            [
                KeyboardButton(text="💧 Товары"),
                KeyboardButton(text="🛒 Корзина"),
            ],
            [
                KeyboardButton(text="✍️ Оставить отзыв"),
                KeyboardButton(text="🔎 Помощь"),
            ],
            [
                KeyboardButton(text="🛠 Настройки"),
            ],
        ]

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        is_persistent=True,
    )


def remove_keyboard() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()