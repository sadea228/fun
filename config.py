#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

# Загрузка переменных окружения
API_TOKEN = os.getenv("BOT_TOKEN")
if not API_TOKEN:
    print("Ошибка: Не задан токен бота. Укажите переменную окружения BOT_TOKEN")
    sys.exit(1)

# Username администратора
ADMIN_USERNAME = "sadea12"

# Public URL для webhook (например https://yourapp.onrender.com)
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
if not WEBHOOK_URL:
    print("Ошибка: Не задан WEBHOOK_URL. Укажите публичный URL сервиса через переменную окружения WEBHOOK_URL")
    sys.exit(1) 