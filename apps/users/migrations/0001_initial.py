from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='TelegramUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_id', models.BigIntegerField(db_index=True, unique=True)),
                ('full_name', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=50)),
                ('language', models.CharField(choices=[('uz', "O'zbekcha"), ('ru', 'Русский')], max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Telegram User',
                'verbose_name_plural': 'Telegram Users',
                'ordering': ('-created_at',),
            },
        ),
    ]
