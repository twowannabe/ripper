import time
import asyncio
from telethon import TelegramClient
from telethon.errors import FloodWaitError
from decouple import config

# Получаем данные из .env файла
api_id = config('API_ID')
api_hash = config('API_HASH')
phone_number = config('PHONE_NUMBER')
chat_ids = config('CHAT_IDS').split(',')

# Создаем клиент Telethon
client = TelegramClient('session_name', api_id, api_hash)

async def delete_all_messages():
    await client.start(phone=phone_number)
    me = await client.get_me()

    for chat_id_str in chat_ids:
        chat_id = int(chat_id_str.strip())
        print(f'Обрабатываем чат с ID {chat_id}')

        messages_to_delete = []
        delay = 0.5  # Начальная задержка в секундах

        async for message in client.iter_messages(chat_id):
            if message.sender_id == me.id:
                messages_to_delete.append(message.id)

                # Пакетное удаление сообщений каждые 100 сообщений
                if len(messages_to_delete) >= 100:
                    while True:
                        try:
                            await client.delete_messages(chat_id, messages_to_delete, revoke=True)
                            print(f'Удалено {len(messages_to_delete)} сообщений в чате {chat_id}')
                            messages_to_delete = []
                            await asyncio.sleep(delay)
                            # Плавно уменьшаем задержку при отсутствии ошибок, но не меньше 0.5 секунд
                            delay = max(0.5, delay * 0.9)
                            break  # Выходим из цикла при успешном удалении
                        except FloodWaitError as e:
                            print(f'Превышен лимит запросов. Ожидание {e.seconds} секунд.')
                            await asyncio.sleep(e.seconds)
                            # Увеличиваем задержку при ошибке
                            delay *= 1.5
                        except Exception as e:
                            print(f'Не удалось удалить сообщения в чате {chat_id}: {e}')
                            break  # Выходим из цикла при других ошибках

        # Удаляем оставшиеся сообщения
        if messages_to_delete:
            while True:
                try:
                    await client.delete_messages(chat_id, messages_to_delete, revoke=True)
                    print(f'Удалено {len(messages_to_delete)} сообщений в чате {chat_id}')
                    await asyncio.sleep(delay)
                    # Плавно уменьшаем задержку при отсутствии ошибок, но не меньше 0.5 секунд
                    delay = max(0.5, delay * 0.9)
                    break
                except FloodWaitError as e:
                    print(f'Превышен лимит запросов. Ожидание {e.seconds} секунд.')
                    await asyncio.sleep(e.seconds)
                    delay *= 1.5
                except Exception as e:
                    print(f'Не удалось удалить сообщения в чате {chat_id}: {e}')
                    break

        # Добавляем задержку между обработкой разных чатов
        await asyncio.sleep(2)

# Запускаем клиент и выполняем функцию удаления
with client:
    client.loop.run_until_complete(delete_all_messages())
