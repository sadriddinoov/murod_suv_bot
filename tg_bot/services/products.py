from asgiref.sync import sync_to_async
from apps.store.models import Product


@sync_to_async
def get_active_products():
    products = Product.objects.filter(is_active=True).prefetch_related("promotions").order_by("id")

    result = []
    for product in products:
        promo = product.promotions.filter(is_active=True).order_by("-id").first()
        discount_percent = promo.discount_percent if promo else 0

        if discount_percent > 0:
            final_price = product.price - (product.price * discount_percent // 100)
        else:
            final_price = product.price

        result.append({
            "id": product.id,
            "name": product.name,
            "name_uz": getattr(product, "name_uz", "") or product.name,
            "name_ru": getattr(product, "name_ru", "") or product.name,
            "volume": product.volume,
            "price": product.price,
            "discount_percent": discount_percent,
            "final_price": final_price,
            "image_path": product.image.path if product.image else None,
        })

    return result


@sync_to_async
def get_product_by_id(product_id: int):
    product = Product.objects.filter(id=product_id, is_active=True).prefetch_related("promotions").first()
    if not product:
        return None

    promo = product.promotions.filter(is_active=True).order_by("-id").first()
    discount_percent = promo.discount_percent if promo else 0

    if discount_percent > 0:
        final_price = product.price - (product.price * discount_percent // 100)
    else:
        final_price = product.price

    return {
        "id": product.id,
        "name": product.name,
        "name_uz": getattr(product, "name_uz", "") or product.name,
        "name_ru": getattr(product, "name_ru", "") or product.name,
        "volume": product.volume,
        "price": product.price,
        "discount_percent": discount_percent,
        "final_price": final_price,
        "image_path": product.image.path if product.image else None,
    }