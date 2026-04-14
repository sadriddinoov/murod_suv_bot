from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile

from tg_bot.services.products import get_active_products, get_product_by_id
from tg_bot.keyboards.inline import products_inline_keyboard, product_card_keyboard
from tg_bot.keyboards.reply import home_keyboard
from tg_bot.services.users import get_user_by_telegram_id

router = Router()


@router.message(F.text.in_(["💧 Mahsulotlar", "💧 Товары"]))
async def products_handler(message: Message):
    products = await get_active_products()

    if not products:
        if message.text == "💧 Mahsulotlar":
            await message.answer("💧 Hozircha mahsulotlar mavjud emas.")
        else:
            await message.answer("💧 Пока товары не добавлены.")
        return

    lang = "uz" if message.text == "💧 Mahsulotlar" else "ru"
    text = "💧 Mahsulotni tanlang:" if lang == "uz" else "💧 Выберите товар:"

    await message.answer(
        text,
        reply_markup=products_inline_keyboard(products, lang)
    )


@router.callback_query(F.data == "show_products")
async def show_products_callback(callback: CallbackQuery):
    products = await get_active_products()

    user = await get_user_by_telegram_id(callback.from_user.id)
    lang = user.language if user else "uz"

    if not products:
        text = "💧 Hozircha mahsulotlar mavjud emas." if lang == "uz" else "💧 Пока товары не добавлены."
        await callback.message.edit_text(text)
        await callback.answer()
        return

    text = "💧 Mahsulotni tanlang:" if lang == "uz" else "💧 Выберите товар:"

    await callback.message.edit_text(
        text,
        reply_markup=products_inline_keyboard(products, lang)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("product_"))
async def product_detail_callback(callback: CallbackQuery):
    product_id = int(callback.data.split("_")[-1])
    product = await get_product_by_id(product_id)

    user = await get_user_by_telegram_id(callback.from_user.id)
    lang = user.language if user else "uz"

    if not product:
        text = "Mahsulot topilmadi" if lang == "uz" else "Товар не найден"
        await callback.answer(text, show_alert=True)
        return

    if lang == "uz":
        text = (
            f"💧 {product['name_uz']}\n"
            f"📦 Hajmi: {product['volume']}\n"
            f"💰 Narxi: {product['price']:,} so'm"
        )
        if product["discount_percent"] > 0:
            text += (
                f"\n🔥 Chegirma: {product['discount_percent']}%"
                f"\n✅ Aksiya narxi: {product['final_price']:,} so'm"
            )
    else:
        text = (
            f"💧 {product['name_ru']}\n"
            f"📦 Объем: {product['volume']}\n"
            f"💰 Цена: {product['price']:,} сум"
        )
        if product["discount_percent"] > 0:
            text += (
                f"\n🔥 Скидка: {product['discount_percent']}%"
                f"\n✅ Цена по акции: {product['final_price']:,} сум"
            )

    if product["image_path"]:
        photo = FSInputFile(product["image_path"])
        await callback.message.answer_photo(
            photo=photo,
            caption=text,
            reply_markup=product_card_keyboard(product["id"], lang)
        )
    else:
        await callback.message.answer(
            text,
            reply_markup=product_card_keyboard(product["id"], lang)
        )

    await callback.answer()


@router.callback_query(F.data == "products_back")
async def products_back_callback(callback: CallbackQuery):
    user = await get_user_by_telegram_id(callback.from_user.id)
    lang = user.language if user else "uz"

    text = (
        "💧 Siz bosh menyudasiz.\nIltimos, kerakli bo'limni tanlang ⬇️"
        if lang == "uz"
        else "💧 Вы в главном меню.\nПожалуйста, выберите нужный раздел ⬇️"
    )

    await callback.message.answer(text, reply_markup=home_keyboard(lang))
    await callback.answer()


@router.callback_query(F.data == "open_cart")
async def open_cart_callback(callback: CallbackQuery):
    user = await get_user_by_telegram_id(callback.from_user.id)
    lang = user.language if user else "uz"

    text = "🛒 Savatcha hozircha bo'sh." if lang == "uz" else "🛒 Корзина пока пустая."
    await callback.answer()
    await callback.message.answer(text)


@router.callback_query(F.data.startswith("add_to_cart_"))
async def add_to_cart_callback(callback: CallbackQuery):
    user = await get_user_by_telegram_id(callback.from_user.id)
    lang = user.language if user else "uz"

    text = "🛒 Mahsulot savatchaga qo'shiladi" if lang == "uz" else "🛒 Товар будет добавлен в корзину"
    await callback.answer(text)