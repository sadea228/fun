#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.types import Update

from config import API_TOKEN, WEBHOOK_URL
import handlers  # регистрация хендлеров
from reactions import start_reactions

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Путь для вебхука
WEBHOOK_PATH = f"/webhook/{API_TOKEN}"

async def handle_webhook(request):
    data = await request.json()
    update = Update(**data)
    await dp.process_update(update)
    return web.Response(text="OK")

async def on_startup(app):
    # Устанавливаем webhook и запускаем цикл реакций
    await bot.set_webhook(url=WEBHOOK_URL + WEBHOOK_PATH)
    await start_reactions()

async def on_shutdown(app):
    await bot.delete_webhook()

# Создаем приложение aiohttp
app = web.Application()
app.router.add_post(WEBHOOK_PATH, handle_webhook)
app.on_startup.append(on_startup)
app.on_cleanup.append(on_shutdown)

if __name__ == '__main__':
    port = int(os.getenv("PORT", "80"))
    web.run_app(app, host="0.0.0.0", port=port) 