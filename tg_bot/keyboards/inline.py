from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


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


def products_inline_keyboard(products, lang: str) -> InlineKeyboardMarkup:
    keyboard = []
    for product in products:
        title = product["name_uz"] if lang == "uz" else product["name_ru"]
        keyboard.append([
            InlineKeyboardButton(text=title, callback_data=f"product_{product['id']}")
        ])

    if lang == "uz":
        keyboard.append([InlineKeyboardButton(text="⬅️ Orqaga", callback_data="products_back")])
        keyboard.append([InlineKeyboardButton(text="🛒 Savatcha", callback_data="open_cart")])
    else:
        keyboard.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="products_back")])
        keyboard.append([InlineKeyboardButton(text="🛒 Корзина", callback_data="open_cart")])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def product_card_keyboard(product_id: int, lang: str) -> InlineKeyboardMarkup:
    if lang == "uz":
        keyboard = [
            [InlineKeyboardButton(text="🛒 Savatchaga qo'shish", callback_data=f"add_to_cart_{product_id}")],
            [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="show_products")],
        ]
    else:
        keyboard = [
            [InlineKeyboardButton(text="🛒 Добавить в корзину", callback_data=f"add_to_cart_{product_id}")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="show_products")],
        ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
