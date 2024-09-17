chat_id = -1002373613951  # ID чата с префиксом -100

async def delete_all_messages():
    await client.start(phone=phone_number)

    async for message in client.iter_messages(chat_id):
        if message.sender_id == (await client.get_me()).id:  # Проверка, что сообщение ваше
            try:
                await client.delete_messages(chat_id, message.id, revoke=True)  # Удаление сообщения для всех
                print(f'Удалено сообщение с ID {message.id}')

                # Добавляем задержку в несколько секунд, чтобы избежать блокировки
                time.sleep(1.5)  # 1.5 секунды задержки между удалениями сообщений
            except Exception as e:
                print(f'Не удалось удалить сообщение с ID {message.id}: {e}')

with client:
    client.loop.run_until_complete(delete_all_messages())
