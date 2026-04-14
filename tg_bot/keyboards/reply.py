from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def language_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🇺🇿 O'zbekcha")],
            [KeyboardButton(text="🇷🇺 Русский")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def phone_keyboard(lang: str):
    text = "📱 Raqamni yuborish" if lang == "uz" else "📱 Поделиться номером"
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=text, request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def home_keyboard(lang: str):
    if lang == "uz":
        keyboard = [
            [
                KeyboardButton(text="💧 Mahsulotlar"),
                KeyboardButton(text="🛒 Savatcha"),
            ],
            [
                KeyboardButton(text="✍️ Fikr qoldirish"),
                KeyboardButton(text="📞 Yordam"),
            ],
            [
                KeyboardButton(text="⚙️ Sozlamalar"),
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
                KeyboardButton(text="📞 Помощь"),
            ],
            [
                KeyboardButton(text="⚙️ Настройки"),
            ],
        ]

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        is_persistent=True,
    )