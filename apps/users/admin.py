from django.contrib import admin
from .models import TelegramUser


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'telegram_id', 'phone', 'language', 'created_at')
    search_fields = ('full_name', 'phone', 'telegram_id')
    list_filter = ('language', 'created_at')
