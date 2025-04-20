#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Модуль хранения текущего состояния бота
# reactions — список доступных реакций
# ignored_users — множество имён пользователей, которых игнорируем
# message_pool — пул сообщений для реакции, формат: [(chat_id, message_id), ...]
# interval_seconds — интервал между реакциями в секундах
# reaction_task — текущая асинхронная задача петли реакций

reactions = ["😂", "👍", "👎", "🖕"]
ignored_users = set()
message_pool = []  # list of tuples (chat_id, message_id)
interval_seconds = 60
reaction_task = None 