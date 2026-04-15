from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from tg_bot.services.products import get_active_products, get_product_by_id
from tg_bot.services.cart import add_product_to_cart, get_user_cart
from tg_bot.keyboards.reply import home_keyboard, products_keyboard, quantity_keyboard
from tg_bot.services.users import get_user_by_telegram_id
from tg_bot.states.product import ProductState

router = Router()


def fmt_price(value: int) -> str:
    return f"{value:,}".replace(",", ".")


@router.message(F.text.in_(["💧 Maxsulotlar", "💧 Товары"]))
async def products_handler(message: Message):
    products = await get_active_products()

    user = await get_user_by_telegram_id(message.from_user.id)
    lang = user.language if user else "uz"

    if not products:
        text = "💧 Hozircha mahsulotlar mavjud emas." if lang == "uz" else "💧 Пока нет товаров."
        await message.answer(text)
        return

    text = "💧 Maxsulotlar:" if lang == "uz" else "💧 Товары:"

    await message.answer(
        text,
        reply_markup=products_keyboard(products, lang)
    )


@router.message(F.text.in_(["⬅️ Orqaga", "⬅️ Назад"]))
async def back_from_products_handler(message: Message, state: FSMContext):
    await state.clear()

    user = await get_user_by_telegram_id(message.from_user.id)
    lang = user.language if user else "uz"

    text = (
        "💧 Siz bosh menyudasiz.\nIltimos, kerakli bo'limni tanlang ⬇️"
        if lang == "uz"
        else "💧 Вы в главном меню.\nПожалуйста, выберите нужный раздел ⬇️"
    )

    await message.answer(text, reply_markup=home_keyboard(lang))


@router.message(F.text.in_(["🛒 Savatcha", "🛒 Корзина"]))
async def cart_handler(message: Message):
    user = await get_user_by_telegram_id(message.from_user.id)
    lang = user.language if user else "uz"

    cart = await get_user_cart(message.from_user.id)

    if not cart or not cart["items"]:
        text = "🛒 Savatcha hozircha bo'sh." if lang == "uz" else "🛒 Корзина пока пустая."
        await message.answer(text)
        return

    if lang == "uz":
        text = "🛒 Savatchangiz:\n\n"
        for item in cart["items"]:
            text += (
            f"💧 {item['name_uz']}\n"
            f"📦 {item['volume']}\n"
            f"🔢 Soni: {item['quantity']}\n"
            f"💰 {fmt_price(item['item_total'])} so'm\n\n"
        )

        text += f"💵 Jami: {fmt_price(cart['subtotal'])} so'm\n"

        if cart["discount_amount"] > 0:
            text += f"🔥 Chegirma: {fmt_price(cart['discount_amount'])} so'm\n"

        text += f"✅ Yakuniy summa: {fmt_price(cart['total_amount'])} so'm"
    else:
        text = "🛒 Ваша корзина:\n\n"
        for item in cart["items"]:
            text += (
            f"💧 {item['name_ru']}\n"
            f"📦 {item['volume']}\n"
            f"🔢 Кол-во: {item['quantity']}\n"
            f"💰 {fmt_price(item['item_total'])} сум\n\n"
        )

        text += f"💵 Сумма: {fmt_price(cart['subtotal'])} сум\n"

        if cart["discount_amount"] > 0:
            text += f"🔥 Скидка: {fmt_price(cart['discount_amount'])} сум\n"

        text += f"✅ Итого: {fmt_price(cart['total_amount'])} сум"

    await message.answer(text)


@router.message(StateFilter(None), F.text)
async def product_detail_handler(message: Message, state: FSMContext):
    user = await get_user_by_telegram_id(message.from_user.id)
    lang = user.language if user else "uz"

    products = await get_active_products()
    product_titles = {
        (p["name_uz"] if lang == "uz" else p["name_ru"]): p["id"]
        for p in products
    }

    if message.text not in product_titles:
        return

    product_id = product_titles[message.text]
    product = await get_product_by_id(product_id)

    if not product:
        text = "Mahsulot topilmadi" if lang == "uz" else "Товар не найден"
        await message.answer(text)
        return

    await state.update_data(selected_product_id=product["id"])
    await state.set_state(ProductState.waiting_for_custom_quantity)

    if lang == "uz":
        text = (
            f"💧 {product['name_uz']}\n"
            f"📦 Hajmi: {product['volume']}\n"
            f"💰 Narxi: {fmt_price(product['price'])} so'm"
        )
        if product["discount_percent"] > 0:
            text += (
                f"\n🔥 Chegirma: {product['discount_percent']}%"
                f"\n✅ Aksiya narxi: {fmt_price(product['final_price'])} so'm"
            )
        text += "\n\n🔢 Kerakli miqdorni tanlang:"
    else:
        text = (
            f"💧 {product['name_ru']}\n"
            f"📦 Объем: {product['volume']}\n"
            f"💰 Цена: {fmt_price(product['price'])} сум"
        )
        if product["discount_percent"] > 0:
            text += (
                f"\n🔥 Скидка: {product['discount_percent']}%"
                f"\n✅ Цена по акции: {fmt_price(product['final_price'])} сум"
            )
        text += "\n\n🔢 Выберите количество:"

    if product["image_path"]:
        photo = FSInputFile(product["image_path"])
        await message.answer_photo(photo=photo, caption=text, reply_markup=quantity_keyboard(lang))
    else:
        await message.answer(text, reply_markup=quantity_keyboard(lang))


@router.message(ProductState.waiting_for_custom_quantity, F.text.in_(["3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]))
async def quantity_selected_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    product_id = data.get("selected_product_id")

    user = await get_user_by_telegram_id(message.from_user.id)
    lang = user.language if user else "uz"

    if not product_id:
        text = "Avval mahsulotni tanlang." if lang == "uz" else "Сначала выберите товар."
        await message.answer(text, reply_markup=home_keyboard(lang))
        await state.clear()
        return

    quantity = int(message.text)
    result = await add_product_to_cart(message.from_user.id, product_id, quantity)

    if not result:
        text = "Mahsulot savatchaga qo'shilmadi." if lang == "uz" else "Товар не добавлен в корзину."
        await message.answer(text, reply_markup=home_keyboard(lang))
        await state.clear()
        return

    text = (
        "🛒 Maxsulot savatchaga qo'shildi.\nBuyurtma berish uchun savatchaga o'ting."
        if lang == "uz"
        else "🛒 Товар добавлен в корзину.\nДля оформления заказа перейдите в корзину."
    )

    await message.answer(text, reply_markup=home_keyboard(lang))
    await state.clear()


@router.message(ProductState.waiting_for_custom_quantity, F.text.in_(["✍️ Boshqa miqdor", "✍️ Другое количество"]))
async def ask_custom_quantity_handler(message: Message):
    user = await get_user_by_telegram_id(message.from_user.id)
    lang = user.language if user else "uz"

    text = (
        "🔢 Kerakli miqdorni raqam bilan yozing:"
        if lang == "uz"
        else "🔢 Напишите нужное количество числом:"
    )
    await message.answer(text)


@router.message(ProductState.waiting_for_custom_quantity, F.text.regexp(r"^\d+$"))
async def custom_quantity_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    product_id = data.get("selected_product_id")

    user = await get_user_by_telegram_id(message.from_user.id)
    lang = user.language if user else "uz"

    if not product_id:
        text = "Avval mahsulotni tanlang." if lang == "uz" else "Сначала выберите товар."
        await message.answer(text, reply_markup=home_keyboard(lang))
        await state.clear()
        return

    quantity = int(message.text)
    if quantity <= 0:
        text = "Miqdor 1 dan katta bo'lishi kerak." if lang == "uz" else "Количество должно быть больше 0."
        await message.answer(text)
        return

    result = await add_product_to_cart(message.from_user.id, product_id, quantity)

    if not result:
        text = "Mahsulot savatchaga qo'shilmadi." if lang == "uz" else "Товар не добавлен в корзину."
        await message.answer(text, reply_markup=home_keyboard(lang))
        await state.clear()
        return

    text = (
        "🛒 Maxsulot savatchaga qo'shildi.\nBuyurtma berish uchun savatchaga o'ting."
        if lang == "uz"
        else "🛒 Товар добавлен в корзину.\nДля оформления заказа перейдите в корзину."
    )

    await message.answer(text, reply_markup=home_keyboard(lang))
    await state.clear()


@router.message(ProductState.waiting_for_custom_quantity)
async def invalid_custom_quantity_handler(message: Message):
    user = await get_user_by_telegram_id(message.from_user.id)
    lang = user.language if user else "uz"

    text = (
        "❌ Faqat raqam kiriting."
        if lang == "uz"
        else "❌ Введите только число."
    )
    await message.answer(text)