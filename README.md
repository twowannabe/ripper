# Telegram Message Ripper

## Описание

Этот проект представляет собой набор скриптов на Python, использующих библиотеку [Telethon](https://github.com/LonamiWebs/Telethon) для автоматического удаления всех сообщений пользователя из заданных чатов в Telegram. Скрипты предназначены для безопасной и эффективной работы с большими объемами сообщений, включая управление лимитами API Telegram.

## Возможности

- Удаление всех сообщений, отправленных текущим пользователем, в одном или нескольких чатах.
- Получение списка ваших групповых чатов и сохранение их ID в файл.
- Обработка ошибок, связанных с правами администратора чата, приватными каналами или отсутствием доступа.
- Интеллектуальное управление частотой запросов для избежания ошибки `FloodWaitError` и блокировок Telegram.
- Подробное логирование процессов, ошибок и удаленных сообщений для удобного мониторинга.
- Возможность настройки скриптов через файл `.env`.

## Установка

1. **Клонируйте репозиторий:**

   ```bash
   git clone git@github.com:twowannabe/ripper.git
   ```

2. **Перейдите в директорию проекта:**

   ```bash
   cd ripper
   ```

3. **Установите зависимости:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Создайте файл `.env`** в корневой директории проекта и заполните его следующими переменными:

   ```plaintext
   API_ID=<ваш_api_id>
   API_HASH=<ваш_api_hash>
   PHONE_NUMBER=<ваш_номер_телефона>
   ```

   - `API_ID` и `API_HASH` можно получить через [Telegram API](https://my.telegram.org/apps).
   - `PHONE_NUMBER` — номер телефона вашего аккаунта Telegram в формате `+1234567890`.

## Использование

### Шаг 1: Получение списка чатов и сохранение их ID

Перед удалением сообщений необходимо получить список ваших групповых чатов и сохранить их ID.

1. **Запустите скрипт `list_chats.py`:**

   ```bash
   python list_chats.py
   ```

   Скрипт выведет в консоль список ваших групповых чатов с их названиями и ID, а также сохранит все ID в файл `chat_ids.env` в формате:

   ```plaintext
   CHAT_IDS=<id_чата1>,<id_чата2>,<id_чата3>,...
   ```

2. **Проверьте файл `chat_ids.env`:**

   Откройте файл и убедитесь, что он содержит ID тех чатов, из которых вы хотите удалить свои сообщения. При необходимости отредактируйте список ID, оставив только нужные вам чаты.

### Шаг 2: Удаление сообщений

1. **Убедитесь, что файл `chat_ids.env` корректен.**

2. **Запустите скрипт `delete_messages.py`:**

   ```bash
   python delete_messages.py
   ```

   Скрипт начнет процесс удаления всех ваших сообщений из указанных чатов. В консоли будет отображаться подробный лог процесса, включая количество удаленных сообщений и возможные ошибки.

## Зависимости

- **Python 3.7+**
- **[Telethon](https://github.com/LonamiWebs/Telethon)**
- **[python-decouple](https://github.com/henriquebastos/python-decouple)**
- **[asyncio](https://docs.python.org/3/library/asyncio.html)**

## Лицензия

Этот проект лицензирован под лицензией MIT. Подробности см. в файле [LICENSE.md](LICENSE.md).

## Вклад

Приветствуются любые вклады и улучшения! Пожалуйста, создайте форк репозитория и отправьте Pull Request.

## Контакты

- **Автор**: [twowannabe](https://github.com/twowannabe)
- **Репозиторий**: [ripper](https://github.com/twowannabe/ripper.git)
