from django.contrib import admin
from django.utils.html import format_html
from modeltranslation.admin import TranslationAdmin

from .models import (
    Product,
    Promotion,
    Cart,
    CartItem,
    Order,
    OrderItem,
    BotSetting,
    Feedback,
    HelpMessage,
)


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    autocomplete_fields = ("product",)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    autocomplete_fields = ("product",)
    readonly_fields = ("unit_price", "discount_percent", "discount_amount", "final_price", "subtotal")

    def subtotal(self, obj):
        return obj.subtotal
    subtotal.short_description = "Subtotal"


@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    list_display = (
        "id",
        "name",
        "volume",
        "price",
        "is_active",
        "image_preview",
        "created_at",
    )
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "name_uz", "name_ru", "volume")
    readonly_fields = ("created_at", "updated_at", "image_preview")
    ordering = ("-id",)
    list_per_page = 20
    date_hierarchy = "created_at"

    fieldsets = (
        ("Asosiy ma'lumot / Основная информация", {
            "fields": ("name", "volume", "price", "image", "image_preview", "is_active")
        }),
        ("Vaqt / Время", {
            "fields": ("created_at", "updated_at")
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="70" height="70" style="border-radius:8px; object-fit:cover;" />', obj.image.url)
        return "-"
    image_preview.short_description = "Preview"


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
    list_filter = ("is_active", "created_at", "start_date", "end_date")
    search_fields = ("product__name", "product__name_uz", "product__name_ru")
    readonly_fields = ("created_by", "created_at", "updated_at")
    ordering = ("-id",)
    list_per_page = 20
    autocomplete_fields = ("product", "created_by")
    date_hierarchy = "created_at"

    fieldsets = (
        ("Promotion info", {
            "fields": ("product", "discount_percent", "is_active")
        }),
        ("Dates", {
            "fields": ("start_date", "end_date")
        }),
        ("System", {
            "fields": ("created_by", "created_at", "updated_at")
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            telegram_user = getattr(request.user, "telegram_user", None)
            if telegram_user:
                obj.created_by = telegram_user
        super().save_model(request, obj, form, change)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "subtotal", "discount_amount", "total_amount", "created_at", "updated_at")
    search_fields = ("user__full_name", "user__phone", "user__telegram_id")
    readonly_fields = ("created_at", "updated_at", "subtotal", "discount_amount", "total_amount")
    inlines = [CartItemInline]
    ordering = ("-id",)
    list_per_page = 20
    date_hierarchy = "created_at"
    autocomplete_fields = ("user",)


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
    list_filter = ("status", "created_at")
    search_fields = ("user__full_name", "user__phone", "phone", "address")
    readonly_fields = ("created_at", "updated_at", "subtotal", "discount_amount", "total_amount")
    inlines = [OrderItemInline]
    ordering = ("-id",)
    list_per_page = 20
    date_hierarchy = "created_at"
    autocomplete_fields = ("user",)

    fieldsets = (
        ("Buyurtma / Заказ", {
            "fields": ("user", "phone", "status")
        }),
        ("Manzil / Адрес", {
            "fields": ("address", "latitude", "longitude", "delivery_time", "comment")
        }),
        ("Hisob / Итоги", {
            "fields": ("subtotal", "discount_amount", "total_amount")
        }),
        ("Vaqt / Время", {
            "fields": ("created_at", "updated_at")
        }),
    )


@admin.register(BotSetting)
class BotSettingAdmin(admin.ModelAdmin):
    list_display = ("id", "operator_telegram_id")
    ordering = ("-id",)

    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "rating", "short_comment", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("user__full_name", "user__phone", "comment")
    ordering = ("-id",)
    list_per_page = 20
    date_hierarchy = "created_at"
    autocomplete_fields = ("user",)
    readonly_fields = ("created_at", "updated_at")

    def short_comment(self, obj):
        if not obj.comment:
            return "-"
        return obj.comment[:50]
    short_comment.short_description = "Comment"


@admin.register(HelpMessage)
class HelpMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "short_text", "created_at")
    search_fields = ("user__full_name", "user__phone", "text")
    ordering = ("-id",)
    list_per_page = 20
    date_hierarchy = "created_at"
    autocomplete_fields = ("user",)

    def short_text(self, obj):
        return obj.text[:60]
    short_text.short_description = "Message"