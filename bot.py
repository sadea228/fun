#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
print("DEBUG: bot.py loaded", f"BOT_TOKEN present: {'yes' if os.getenv('BOT_TOKEN') else 'no'}", f"WEBHOOK_URL present: {'yes' if os.getenv('WEBHOOK_URL') else 'no'}")
print(f"WEBHOOK_URL value: {os.getenv('WEBHOOK_URL')}")
import logging
logging.basicConfig(level=logging.DEBUG)
import asyncio
from aiohttp import web, ClientSession
from aiogram import Bot, Dispatcher, types
from aiogram.types import Update, BotCommand

from config import API_TOKEN, WEBHOOK_URL
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Регистрируем хендлеры и реакции после создания bot и dp, чтобы избежать circular import
import handlers  # регистрация хендлеров
from reactions import start_reactions

# Путь для вебхука
WEBHOOK_PATH = f"/webhook/{API_TOKEN}"

async def handle_webhook(request):
    # Respond OK to non-POST requests (health checks / Telegram GET/HEAD)
    if request.method != 'POST':
        return web.Response(text="OK")
    try:
        data = await request.json()
        logging.info(f"<<< update: {data}")
        update = Update(**data)
        await dp.process_update(update)
        return web.Response(text="OK")
    except Exception as e:
        logging.error(f"Error processing update: {e}")
        import traceback
        logging.error(traceback.format_exc())
        return web.Response(text="Error", status=500)

async def on_startup(app):
    # Устанавливаем webhook и запускаем цикл реакций
    # Нормализуем WEBHOOK_URL и логируем полную ссылку
    webhook_url = WEBHOOK_URL.rstrip('/') + WEBHOOK_PATH
    logging.info(f"Setting webhook to {webhook_url}")
    # Сбрасываем все ожидающие обновления
    await bot.set_webhook(url=webhook_url, drop_pending_updates=True)
    # Получаем информацию о webhook и логируем её
    info = await bot.get_webhook_info()
    logging.info(f"Webhook info: url={info.url}, pending_updates={info.pending_update_count}, last_error={info.last_error_message}, last_error_date={info.last_error_date}")
    # Регистрируем команды для автодополнения при вводе "/"
    commands = [
        BotCommand("add_reaction", "Добавить эмодзи в пул реакций"),
        BotCommand("remove_reaction", "Удалить эмодзи из пула реакций"),
        BotCommand("list_reactions", "Показать пул реакций"),
        BotCommand("set_interval", "Установить интервал в секундах"),
        BotCommand("ignore_user", "Игнорировать пользователя"),
        BotCommand("unignore_user", "Убрать пользователя из игнор-листа"),
        BotCommand("list_ignored", "Показать игнор-лист"),
        BotCommand("restart_reactions", "Перезапустить таймер реакций"),
    ]
    await bot.set_my_commands(commands)
    await start_reactions()

async def on_shutdown(app):
    await bot.delete_webhook()

# Добавим корневой обработчик для проверки статуса сервиса
async def handle_root(request):
    return web.Response(text="Bot is running")

# Создаем приложение aiohttp
app = web.Application()
app.router.add_route('*', '/', handle_root)
app.router.add_route('*', WEBHOOK_PATH, handle_webhook)
app.on_startup.append(on_startup)
app.on_cleanup.append(on_shutdown)

# Добавим простой обработчик для любых сообщений
@dp.message_handler()
async def echo_message(message):
    logging.info(f"Received message: {message.text} from {message.from_user.username or message.from_user.id}")
    await message.reply(f"Вы написали: {message.text}")

# Добавим команду для тестирования активности бота
@dp.message_handler(commands=['ping'])
async def cmd_ping(message: types.Message):
    logging.info("Ping command received")
    await message.reply("Pong! Бот активен и реагирует на команды.")
    # Тестируем соединение с Telegram API
    async with ClientSession() as session:
        async with session.get(f"https://api.telegram.org/bot{API_TOKEN}/getMe") as resp:
            if resp.status == 200:
                result = await resp.json()
                await message.reply(f"Соединение с Telegram API в порядке. Ответ: {result}")
            else:
                await message.reply(f"Ошибка соединения с Telegram API: {resp.status}")

if __name__ == '__main__':
    port = int(os.getenv("PORT", "80"))
    web.run_app(app, host="0.0.0.0", port=port) 