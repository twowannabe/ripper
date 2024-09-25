import time
import asyncio
import logging
from telethon import TelegramClient
from telethon.errors import FloodWaitError
from telethon.errors.rpcerrorlist import ChatAdminRequiredError, ChannelPrivateError
from decouple import config

# Настраиваем логирование
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Получаем данные из .env файла
api_id = config('API_ID')
api_hash = config('API_HASH')
phone_number = config('PHONE_NUMBER')

# Считываем chat_ids из файла chat_ids.env
chat_ids_file = 'chat_ids.env'
chat_ids = []
with open(chat_ids_file, 'r') as file:
    for line in file:
        if line.startswith('CHAT_IDS'):
            chat_ids = line.split('=')[1].strip().split(',')

# Создаем клиент Telethon
client = TelegramClient('session_name', api_id, api_hash)

async def delete_all_messages():
    await client.start(phone=phone_number)
    me = await client.get_me()
    total_deleted = 0  # Счетчик удаленных сообщений

    for chat_id_str in chat_ids:
        chat_id = int(chat_id_str.strip())

        try:
            # Проверяем доступность чата
            entity = await client.get_entity(chat_id)

            # Получаем название чата
            if hasattr(entity, 'title') and entity.title:
                chat_name = entity.title
            elif hasattr(entity, 'first_name') and entity.first_name:
                chat_name = entity.first_name
            else:
                chat_name = 'Без названия'

            logging.info(f'Обрабатываем чат "{chat_name}" (ID {chat_id})')

        except ValueError as e:
            logging.error(f'Чат с ID {chat_id} не найден: {e}')
            continue
        except (ChatAdminRequiredError, ChannelPrivateError) as e:
            logging.error(f'Нет доступа к чату с ID {chat_id}: {e}')
            continue
        except Exception as e:
            logging.error(f'Не удалось получить чат с ID {chat_id}: {e}')
            continue

        messages_to_delete = []
        delay = 0.5  # Начальная задержка в секундах

        offset_id = 0
        limit = 100  # Количество сообщений, получаемых за один запрос

        while True:
            try:
                # Получаем сообщения от пользователя
                history = await client.get_messages(chat_id, limit=limit, offset_id=offset_id, from_user='me')
                if not history:
                    logging.info(f'Нет сообщений для удаления в чате "{chat_name}" (ID {chat_id}). Пропускаем.')
                    break  # Если сообщений больше нет, выходим из цикла

                for message in history:
                    messages_to_delete.append(message.id)

                if messages_to_delete:
                    logging.info(f'Готовим к удалению сообщения с ID: {messages_to_delete}')
                    while True:
                        try:
                            await client.delete_messages(chat_id, messages_to_delete, revoke=True)
                            total_deleted += len(messages_to_delete)  # Обновляем счетчик
                            logging.info(f'Удалено {len(messages_to_delete)} сообщений в чате "{chat_name}" (ID {chat_id})')
                            logging.info(f'Всего удалено сообщений: {total_deleted}')
                            messages_to_delete = []
                            await asyncio.sleep(delay)
                            delay = max(0.5, delay * 0.9)
                            break
                        except FloodWaitError as e:
                            logging.warning(f'Превышен лимит запросов. Ожидание {e.seconds} секунд.')
                            await asyncio.sleep(e.seconds)
                            delay *= 1.5
                        except Exception as e:
                            logging.error(f'Не удалось удалить сообщения в чате "{chat_name}" (ID {chat_id}): {e}')
                            break

                # Обновляем offset_id для следующего запроса
                offset_id = history[-1].id
                await asyncio.sleep(0.1)  # Небольшая задержка между запросами

            except FloodWaitError as e:
                logging.warning(f'Превышен лимит запросов при получении сообщений. Ожидание {e.seconds} секунд.')
                await asyncio.sleep(e.seconds)
            except Exception as e:
                logging.error(f'Ошибка при получении сообщений из чата "{chat_name}" (ID {chat_id}): {e}')
                break

        # Добавляем задержку между обработкой разных чатов
        await asyncio.sleep(2)

    logging.info(f'Операция завершена, всего удалено сообщений: {total_deleted}')

# Запускаем клиент и выполняем функцию удаления
with client:
    client.loop.run_until_complete(delete_all_messages())
