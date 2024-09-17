import time
from telethon import TelegramClient
from decouple import config

# Получаем данные из .env файла
api_id = config('API_ID')  # ID API из вашего приложения Telegram
api_hash = config('API_HASH')  # Hash API из вашего приложения Telegram
phone_number = config('PHONE_NUMBER')  # Ваш номер телефона, зарегистрированный в Telegram

# Создаем клиент Telethon
client = TelegramClient('session_name', api_id, api_hash)

async def delete_all_messages():
    await client.start(phone=phone_number)

    chat_id = -1002373613951  # Используем правильный ID чата для приватного чата

    async for message in client.iter_messages(chat_id):
        if message.sender_id == (await client.get_me()).id:  # Проверка, что сообщение ваше
            try:
                await client.delete_messages(chat_id, message.id, revoke=True)  # Удаление сообщения для всех
                print(f'Удалено сообщение с ID {message.id}')

                # Добавляем задержку в несколько секунд, чтобы избежать блокировки
                time.sleep(1.5)  # Задержка в 1.5 секунды между удалениями сообщений
            except Exception as e:
                print(f'Не удалось удалить сообщение с ID {message.id}: {e}')

# Запускаем клиент и выполняем функцию удаления
with client:
    client.loop.run_until_complete(delete_all_messages())
