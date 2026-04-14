from django.db import models


class TelegramUser(models.Model):
    LANGUAGE_CHOICES = (
        ('uz', "O'zbekcha"),
        ('ru', 'Русский'),
    )

    telegram_id = models.BigIntegerField(unique=True, db_index=True)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Telegram User'
        verbose_name_plural = 'Telegram Users'
        ordering = ('-created_at',)

    def __str__(self):
        return f"{self.full_name} ({self.telegram_id})"
