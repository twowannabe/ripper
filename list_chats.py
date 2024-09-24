from telethon import TelegramClient
from decouple import config
import os

# Получаем данные из .env файла
api_id = config('API_ID')
api_hash = config('API_HASH')
phone_number = config('PHONE_NUMBER')
chat_ids_file = 'chat_ids.env'  # Файл для хранения chat_ids

# Создаем клиент Telethon
client = TelegramClient('session_name', api_id, api_hash)

async def list_chats():
    await client.start(phone=phone_number)

    chat_ids = []  # Список для хранения chat_id

    # Проходим по всем диалогам (чатам, каналам, группам)
    async for dialog in client.iter_dialogs():
        chat_id = dialog.id
        chat_name = dialog.name

        # Фильтруем только группы
        if dialog.is_group:
            # Если чат приватный, то ID начинается с -100
            if chat_id < 0:
                chat_id = f"-100{abs(chat_id)}"

            print(f'Название: {chat_name}, ID: {chat_id}')
            chat_ids.append(chat_id)  # Добавляем chat_id в список

    # Преобразуем список chat_ids в строку для записи в файл
    chat_ids_str = ','.join(str(id) for id in chat_ids)

    # Записываем chat_ids в новый файл в формате переменной
    with open(chat_ids_file, 'w') as file:
        file.write(f'CHAT_IDS={chat_ids_str}\n')

    print(f"Сохранено в файл {chat_ids_file}: {chat_ids_str}")

# Запускаем клиент и выполняем функцию получения списка чатов
with client:
    client.loop.run_until_complete(list_chats())
