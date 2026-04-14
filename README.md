# Murod Suv Bot — Django + aiogram + SQLite

## Stack
- Django — models, admin panel, SQLite
- aiogram — Telegram bot
- SQLite — local development

## Setup
1. Create virtualenv and activate it.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and set your bot token.
4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```
6. Run Django admin:
   ```bash
   python manage.py runserver
   ```
7. In another terminal run bot:
   ```bash
   python bot.py
   ```

## Admin URL
- http://127.0.0.1:8000/admin

## Current features
- /start
- language selection (UZ/RU)
- phone request
- saving user to Django database
- opening home menu after registration
- repeat /start opens home directly

## Next steps
- products app
- promotions
- orders
- operator settings
