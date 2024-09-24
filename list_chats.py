from telethon import TelegramClient
from decouple import config

# Получаем данные из .env файла
api_id = config('API_ID')
api_hash = config('API_HASH')
phone_number = config('PHONE_NUMBER')

# Создаем клиент Telethon
client = TelegramClient('session_name', api_id, api_hash)

async def list_chats():
    await client.start(phone=phone_number)

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

# Запускаем клиент и выполняем функцию получения списка чатов
with client:
    client.loop.run_until_complete(list_chats())
