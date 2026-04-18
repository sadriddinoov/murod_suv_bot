from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="telegramuser",
            options={
                "ordering": ("-created_at",),
                "verbose_name": "Telegram user",
                "verbose_name_plural": "Telegram users",
            },
        ),
        migrations.AlterField(
            model_name="telegramuser",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Created at"),
        ),
        migrations.AlterField(
            model_name="telegramuser",
            name="full_name",
            field=models.CharField(max_length=255, verbose_name="Full name"),
        ),
        migrations.AlterField(
            model_name="telegramuser",
            name="language",
            field=models.CharField(
                choices=[("uz", "O'zbekcha"), ("ru", "Русский")],
                max_length=10,
                verbose_name="Language",
            ),
        ),
        migrations.AlterField(
            model_name="telegramuser",
            name="phone",
            field=models.CharField(max_length=50, verbose_name="Phone"),
        ),
        migrations.AlterField(
            model_name="telegramuser",
            name="telegram_id",
            field=models.BigIntegerField(db_index=True, unique=True, verbose_name="Telegram ID"),
        ),
        migrations.AlterField(
            model_name="telegramuser",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, verbose_name="Updated at"),
        ),
    ]
