#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from aiogram import types
from bot import dp

import state
from config import ADMIN_USERNAME
from reactions import restart_reactions

# Проверка администратора

def is_admin(message: types.Message) -> bool:
    return message.from_user.username == ADMIN_USERNAME

# Сбор новых сообщений
@dp.message_handler(content_types=types.ContentType.TEXT)
async def collect_messages(message: types.Message):
    if (message.from_user.is_bot
        or message.text.startswith("/")
        or (message.from_user.username and message.from_user.username in state.ignored_users)):
        return
    state.message_pool.append((message.chat.id, message.message_id))

# Команды администратора
@dp.message_handler(commands=['add_reaction'])
async def cmd_add_reaction(message: types.Message):
    if not is_admin(message):
        return
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.reply("Использование: /add_reaction 😂")
        return
    emoji = parts[1].strip()
    if emoji in state.reactions:
        await message.reply("Эмодзи уже в пуле.")
    else:
        state.reactions.append(emoji)
        await message.reply(f"Добавлено {emoji} в пул реакций.")

@dp.message_handler(commands=['remove_reaction'])
async def cmd_remove_reaction(message: types.Message):
    if not is_admin(message):
        return
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.reply("Использование: /remove_reaction 😂")
        return
    emoji = parts[1].strip()
    if emoji in state.reactions:
        state.reactions.remove(emoji)
        await message.reply(f"Убрано {emoji} из пула реакций.")
    else:
        await message.reply("Эмодзи не найдено в пуле.")

@dp.message_handler(commands=['list_reactions'])
async def cmd_list_reactions(message: types.Message):
    if not is_admin(message):
        return
    await message.reply("Пул реакций: " + ", ".join(state.reactions))

@dp.message_handler(commands=['set_interval'])
async def cmd_set_interval(message: types.Message):
    if not is_admin(message):
        return
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2 or not parts[1].isdigit():
        await message.reply("Использование: /set_interval <секунды>")
        return
    interval_val = int(parts[1])
    if interval_val < 1:
        await message.reply("Интервал должен быть положительным.")
        return
    state.interval_seconds = interval_val
    await message.reply(f"Интервал установлен на {interval_val} секунд.")

@dp.message_handler(commands=['ignore_user'])
async def cmd_ignore_user(message: types.Message):
    if not is_admin(message):
        return
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.reply("Использование: /ignore_user @username")
        return
    username = parts[1].lstrip("@")
    state.ignored_users.add(username)
    await message.reply(f"Пользователь @{username} добавлен в игнор-лист.")

@dp.message_handler(commands=['unignore_user'])
async def cmd_unignore_user(message: types.Message):
    if not is_admin(message):
        return
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.reply("Использование: /unignore_user @username")
        return
    username = parts[1].lstrip("@")
    if username in state.ignored_users:
        state.ignored_users.remove(username)
        await message.reply(f"Пользователь @{username} удален из игнор-листа.")
    else:
        await message.reply(f"Пользователь @{username} нет в игнор-листе.")

@dp.message_handler(commands=['list_ignored'])
async def cmd_list_ignored(message: types.Message):
    if not is_admin(message):
        return
    if state.ignored_users:
        await message.reply("Игнор-лист: " + ", ".join("@" + u for u in state.ignored_users))
    else:
        await message.reply("Игнор-лист пуст.")

@dp.message_handler(commands=['restart_reactions'])
async def cmd_restart_reactions(message: types.Message):
    if not is_admin(message):
        return
    await restart_reactions()
    await message.reply("Таймер реакций перезапущен.") 