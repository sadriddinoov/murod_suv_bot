from asgiref.sync import sync_to_async
from apps.users.models import TelegramUser
from apps.store.models import Cart, CartItem, Product


@sync_to_async
def add_product_to_cart(telegram_id: int, product_id: int, quantity: int):
    user = TelegramUser.objects.filter(telegram_id=telegram_id).first()
    if not user:
        return None

    cart, _ = Cart.objects.get_or_create(user=user)
    product = Product.objects.filter(id=product_id, is_active=True).first()
    if not product:
        return None

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={"quantity": quantity},
    )

    if not created:
        item.quantity += quantity
        item.save()

    return {
        "product_id": product.id,
        "quantity": item.quantity,
    }


@sync_to_async
def get_user_cart(telegram_id: int):
    user = TelegramUser.objects.filter(telegram_id=telegram_id).first()
    if not user:
        return None

    cart = Cart.objects.filter(user=user).prefetch_related("items__product__promotions").first()
    if not cart:
        return {
            "items": [],
            "subtotal": 0,
            "discount_amount": 0,
            "total_amount": 0,
        }

    items_data = []
    subtotal = 0
    discount_amount = 0
    total_amount = 0

    for item in cart.items.all():
        product = item.product
        promo = product.promotions.filter(is_active=True).order_by("-id").first()
        discount_percent = promo.discount_percent if promo else 0

        if discount_percent > 0:
            final_price = product.price - (product.price * discount_percent // 100)
        else:
            final_price = product.price

        item_subtotal = product.price * item.quantity
        item_total = final_price * item.quantity
        item_discount = item_subtotal - item_total

        subtotal += item_subtotal
        discount_amount += item_discount
        total_amount += item_total

        items_data.append({
            "name_uz": getattr(product, "name_uz", "") or product.name,
            "name_ru": getattr(product, "name_ru", "") or product.name,
            "volume": product.volume,
            "quantity": item.quantity,
            "item_total": item_total,
        })

    return {
        "items": items_data,
        "subtotal": subtotal,
        "discount_amount": discount_amount,
        "total_amount": total_amount,
    }