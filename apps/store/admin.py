from django.contrib import admin
from .models import Product, Promotion, Cart, CartItem, Order, OrderItem, BotSetting


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "volume", "price", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name", "name_uz", "name_ru", "volume")


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product",
        "discount_percent",
        "is_active",
        "created_by",
        "start_date",
        "end_date",
        "created_at",
    )
    list_filter = ("is_active", "created_at")
    search_fields = ("product__name", "product__name_uz", "product__name_ru")
    readonly_fields = ("created_by", "created_at", "updated_at")

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            telegram_user = getattr(request.user, "telegram_user", None)
            if telegram_user:
                obj.created_by = telegram_user
        super().save_model(request, obj, form, change)


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at", "updated_at")
    inlines = [CartItemInline]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "phone",
        "status",
        "subtotal",
        "discount_amount",
        "total_amount",
        "created_at",
    )
    list_filter = ("status",)
    search_fields = ("user__full_name", "user__phone", "phone", "address")
    inlines = [OrderItemInline]


@admin.register(BotSetting)
class BotSettingAdmin(admin.ModelAdmin):
    list_display = ("id", "operator_telegram_id")