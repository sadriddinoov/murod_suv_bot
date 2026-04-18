from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)


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
                KeyboardButton(text="💧 Maxsulotlar"),
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


def products_keyboard(products, lang: str):
    keyboard = []

    row = []
    for product in products:
        title = product["name_uz"] if lang == "uz" else product["name_ru"]
        row.append(KeyboardButton(text=title))

        if len(row) == 2:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)

    if lang == "uz":
        keyboard.append([
            KeyboardButton(text="⬅️ Orqaga"),
            KeyboardButton(text="🛒 Savatcha"),
        ])
    else:
        keyboard.append([
            KeyboardButton(text="⬅️ Назад"),
            KeyboardButton(text="🛒 Корзина"),
        ])

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        is_persistent=True,
    )


def quantity_keyboard(lang: str):
    keyboard = [
        [
            KeyboardButton(text="3"),
            KeyboardButton(text="4"),
            KeyboardButton(text="5"),
        ],
        [
            KeyboardButton(text="6"),
            KeyboardButton(text="7"),
            KeyboardButton(text="8"),
        ],
        [
            KeyboardButton(text="9"),
            KeyboardButton(text="10"),
            KeyboardButton(text="11"),
        ],
    ]

    if lang == "uz":
        keyboard.append([
            KeyboardButton(text="12"),
            KeyboardButton(text="✍️ Boshqa miqdor"),
        ])
    else:
        keyboard.append([
            KeyboardButton(text="12"),
            KeyboardButton(text="✍️ Другое количество"),
        ])

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        is_persistent=True,
    )


def settings_keyboard(lang: str):
    if lang == "uz":
        keyboard = [
            [KeyboardButton(text="🌐 Tilni o'zgartirish")],
            [KeyboardButton(text="⬅️ Orqaga")],
        ]
    else:
        keyboard = [
            [KeyboardButton(text="🌐 Сменить язык")],
            [KeyboardButton(text="⬅️ Назад")],
        ]

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        is_persistent=True,
    )


def change_language_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🇺🇿 O'zbekcha")],
            [KeyboardButton(text="🇷🇺 Русский")],
        ],
        resize_keyboard=True,
        is_persistent=True,
    )


def feedback_keyboard(lang: str):
    if lang == "uz":
        keyboard = [
            [KeyboardButton(text="Hammasi yoqdi ❤️")],
            [KeyboardButton(text="Yaxshi ⭐⭐⭐⭐⭐")],
            [KeyboardButton(text="Yoqmadi ⭐⭐⭐")],
            [KeyboardButton(text="Yomon ⭐⭐")],
            [KeyboardButton(text="Juda yomon 👎🏻")],
            [KeyboardButton(text="⬅️ Orqaga")],
        ]
    else:
        keyboard = [
            [KeyboardButton(text="Очень понравилось ❤️")],
            [KeyboardButton(text="Хорошо ⭐⭐⭐⭐⭐")],
            [KeyboardButton(text="Не понравилось ⭐⭐⭐")],
            [KeyboardButton(text="Плохо ⭐⭐")],
            [KeyboardButton(text="Очень плохо 👎🏻")],
            [KeyboardButton(text="⬅️ Назад")],
        ]

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        is_persistent=True,
    )

def cancel_keyboard(lang: str):
    if lang == "uz":
        keyboard = [[KeyboardButton(text="Bekor qilish")]]
    else:
        keyboard = [[KeyboardButton(text="Отмена")]]

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        is_persistent=True,
    )
    
    

def help_inline_keyboard(lang: str) -> InlineKeyboardMarkup:
    if lang == "uz":
        keyboard = [
            [
                InlineKeyboardButton(text="📞 Telefon orqali bog'lanish", callback_data="help_phone"),
                InlineKeyboardButton(text="📬 Xabar jo'natish", callback_data="help_message"),
            ],
            [
                InlineKeyboardButton(text="🛒 Buyurtma tarixi", callback_data="help_orders"),
                InlineKeyboardButton(text="⬅️ Orqaga", callback_data="help_back"),
            ],
        ]
    else:
        keyboard = [
            [
                InlineKeyboardButton(text="📞 Связаться по телефону", callback_data="help_phone"),
                InlineKeyboardButton(text="📬 Отправить сообщение", callback_data="help_message"),
            ],
            [
                InlineKeyboardButton(text="🛒 История заказов", callback_data="help_orders"),
                InlineKeyboardButton(text="⬅️ Назад", callback_data="help_back"),
            ],
        ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
