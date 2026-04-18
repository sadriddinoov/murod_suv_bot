from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin as UnfoldModelAdmin

from .models import TelegramUser


class TelegramUserAdminForm(forms.ModelForm):
    class Meta:
        model = TelegramUser
        fields = "__all__"
        labels = {
            "telegram_id": _("Telegram ID"),
            "full_name": _("Full name"),
            "phone": _("Phone"),
            "language": _("Language"),
        }


class UserLanguageFilter(admin.SimpleListFilter):
    title = _("Language")
    parameter_name = "language"

    def lookups(self, request, model_admin):
        return TelegramUser.LANGUAGE_CHOICES

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(language=self.value())
        return queryset


@admin.register(TelegramUser)
class TelegramUserAdmin(UnfoldModelAdmin):
    form = TelegramUserAdminForm
    list_display = (
        "id",
        "full_name_value",
        "telegram_id_value",
        "phone_value",
        "language_value",
        "created_at_value",
    )
    search_fields = ("full_name", "phone", "telegram_id")
    list_filter = (UserLanguageFilter,)
    readonly_fields = ("created_at_value", "updated_at_value")
    ordering = ("-created_at",)
    list_per_page = 20
    date_hierarchy = "created_at"
    fieldsets = (
        (None, {"fields": ("telegram_id", "full_name", "phone", "language")}),
        (_("Dates"), {"fields": ("created_at_value", "updated_at_value")}),
    )

    @admin.display(ordering="full_name", description=_("Full name"))
    def full_name_value(self, obj):
        return obj.full_name

    @admin.display(ordering="telegram_id", description=_("Telegram ID"))
    def telegram_id_value(self, obj):
        return obj.telegram_id

    @admin.display(ordering="phone", description=_("Phone"))
    def phone_value(self, obj):
        return obj.phone

    @admin.display(ordering="language", description=_("Language"))
    def language_value(self, obj):
        return obj.get_language_display()

    @admin.display(ordering="created_at", description=_("Created at"))
    def created_at_value(self, obj):
        return obj.created_at

    @admin.display(ordering="updated_at", description=_("Updated at"))
    def updated_at_value(self, obj):
        return obj.updated_at
