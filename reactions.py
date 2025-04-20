#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import random
from aiogram.utils import exceptions

import state

async def reaction_loop():
    from bot import bot
    try:
        while True:
            await asyncio.sleep(state.interval_seconds)
            if not state.message_pool:
                continue
            chat_id, msg_id = random.choice(state.message_pool)
            state.message_pool.remove((chat_id, msg_id))
            emoji = random.choice(state.reactions)
            try:
                await bot.send_message(chat_id=chat_id, text=emoji, reply_to_message_id=msg_id)
            except exceptions.TelegramAPIError:
                pass
    except asyncio.CancelledError:
        return

async def start_reactions():
    # Запуск петли реакций, сохранение задачи в state
    state.reaction_task = asyncio.create_task(reaction_loop())

async def restart_reactions():
    # Перезапуск цикла реакций
    if state.reaction_task:
        state.reaction_task.cancel()
    state.reaction_task = asyncio.create_task(reaction_loop()) 