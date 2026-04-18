from django.db import models
from django.utils.translation import gettext_lazy as _


class TelegramUser(models.Model):
    LANGUAGE_CHOICES = (
        ("uz", "O'zbekcha"),
        ("ru", "Русский"),
    )

    telegram_id = models.BigIntegerField(_("Telegram ID"), unique=True, db_index=True)
    full_name = models.CharField(_("Full name"), max_length=255)
    phone = models.CharField(_("Phone"), max_length=50)
    language = models.CharField(_("Language"), max_length=10, choices=LANGUAGE_CHOICES)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        verbose_name = _("Telegram user")
        verbose_name_plural = _("Telegram users")
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.full_name} ({self.telegram_id})"
