from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin
from unfold.admin import ModelAdmin as UnfoldModelAdmin

from .models import BotSetting, Cart, CartItem, Feedback, HelpMessage, Order, OrderItem, Product, Promotion


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    autocomplete_fields = ("product",)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    autocomplete_fields = ("product",)
    readonly_fields = ("unit_price", "discount_percent", "discount_amount", "final_price", "subtotal")

    @admin.display(description=_("Subtotal"))
    def subtotal(self, obj):
        return obj.subtotal


@admin.register(Product)
class ProductAdmin(TranslationAdmin, UnfoldModelAdmin):
    list_display = ("id", "name", "volume", "price", "is_active", "image_preview", "created_at")
    list_display_links = ("name",)
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "name_uz", "name_ru", "name_en", "volume")
    readonly_fields = ("created_at", "updated_at", "image_preview")
    ordering = ("-id",)
    list_per_page = 20
    date_hierarchy = "created_at"
    fieldsets = (
        (_("Main information"), {"fields": ("name", "volume", "price", "image", "image_preview", "is_active")}),
        (_("Dates"), {"fields": ("created_at", "updated_at")}),
    )

    @admin.display(description=_("Preview"))
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<a href="{0}" target="_blank" rel="noopener">'
                '<img src="{0}" width="70" height="70" style="border-radius:8px; object-fit:cover;" />'
                "</a>",
                obj.image.url,
            )
        return "-"


@admin.register(Promotion)
class PromotionAdmin(UnfoldModelAdmin):
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
    list_display_links = ("product",)
    list_filter = ("is_active", "created_at", "start_date", "end_date")
    search_fields = ("product__name", "product__name_uz", "product__name_ru", "product__name_en")
    readonly_fields = ("created_by", "created_at", "updated_at")
    ordering = ("-id",)
    list_per_page = 20
    autocomplete_fields = ("product", "created_by")
    date_hierarchy = "created_at"
    fieldsets = (
        (_("Main information"), {"fields": ("product", "discount_percent", "is_active")}),
        (_("Dates"), {"fields": ("start_date", "end_date")}),
        (_("System information"), {"fields": ("created_by", "created_at", "updated_at")}),
    )

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            telegram_user = getattr(request.user, "telegram_user", None)
            if telegram_user:
                obj.created_by = telegram_user
        super().save_model(request, obj, form, change)


@admin.register(Cart)
class CartAdmin(UnfoldModelAdmin):
    list_display = ("id", "user", "subtotal", "discount_amount", "total_amount", "created_at", "updated_at")
    search_fields = ("user__full_name", "user__phone", "user__telegram_id")
    readonly_fields = ("created_at", "updated_at", "subtotal", "discount_amount", "total_amount")
    list_display_links = ("user",)
    inlines = [CartItemInline]
    ordering = ("-id",)
    list_per_page = 20
    date_hierarchy = "created_at"
    autocomplete_fields = ("user",)


@admin.register(Order)
class OrderAdmin(UnfoldModelAdmin):
    list_display = ("id", "user", "phone", "status", "subtotal", "discount_amount", "total_amount", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("user__full_name", "user__phone", "phone", "address")
    list_display_links = ("user",)
    readonly_fields = ("created_at", "updated_at", "subtotal", "discount_amount", "total_amount")
    inlines = [OrderItemInline]
    ordering = ("-id",)
    list_per_page = 20
    date_hierarchy = "created_at"
    autocomplete_fields = ("user",)
    fieldsets = (
        (_("Order details"), {"fields": ("user", "phone", "status")}),
        (_("Address and delivery"), {"fields": ("address", "latitude", "longitude", "delivery_time", "comment")}),
        (_("Totals"), {"fields": ("subtotal", "discount_amount", "total_amount")}),
        (_("Dates"), {"fields": ("created_at", "updated_at")}),
    )


@admin.register(BotSetting)
class BotSettingAdmin(UnfoldModelAdmin):
    list_display = ("id", "operator_telegram_id_safe")
    ordering = ("-id",)

    @admin.display(description=_("Operator Telegram ID"))
    def operator_telegram_id_safe(self, obj):
        value = getattr(obj, "operator_telegram_id", None)
        return value if value else "-"

    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)


@admin.register(Feedback)
class FeedbackAdmin(UnfoldModelAdmin):
    list_display = ("id", "user", "rating", "short_comment", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("user__full_name", "user__phone", "comment")
    list_display_links = ("id",)
    ordering = ("-id",)
    list_per_page = 20
    date_hierarchy = "created_at"
    autocomplete_fields = ("user",)
    readonly_fields = ("created_at", "updated_at")

    @admin.display(description=_("Comment"))
    def short_comment(self, obj):
        if not obj.comment:
            return "-"
        return obj.comment[:50]


@admin.register(HelpMessage)
class HelpMessageAdmin(UnfoldModelAdmin):
    list_display = ("id", "user", "short_text", "created_at")
    search_fields = ("user__full_name", "user__phone", "text")
    list_display_links = ("id",)
    ordering = ("-id",)
    list_per_page = 20
    date_hierarchy = "created_at"
    autocomplete_fields = ("user",)

    @admin.display(description=_("Text"))
    def short_text(self, obj):
        if not obj.text:
            return "-"
        return obj.text[:60]
