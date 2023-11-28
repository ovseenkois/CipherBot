# CipherBot
# ШифроБот

Приветствую! Это КриптоБот - телеграм-бот для шифрования и расшифровки сообщений с использованием различных методов шифрования. Бот предоставляет пользователю возможность выбирать между тремя методами шифрования: Шифр Цезаря, Шифр Виженера и Шифр Вернама.

## Инструкции по использованию

1. **Шифр Цезаря (/caesar):**
   - Введите /caesar, выберите язык, операцию (зашифровать или дешифровать), укажите сдвиг (ключ) и введите текст.

2. **Шифр Виженера (/visener):**
   - Введите /visener, выберите язык, операцию (зашифровать или дешифровать), введите ключ (строку) и текст.

3. **Шифр Вернама (/vernam):**
   - Введите /vernam, введите текст и сгенерируйте одноразовый ключ.

## Как запустить бота

1. Запустите бота: `python bot.py`

## Дополнительная информация

- Данный бот был разработан с использованием библиотеки Aiogram для работы с Telegram API.
- Алфавиты для шифрования хранятся в отдельном модуле alphabets.py.

## Помощь

Если у вас возникли вопросы или проблемы, не стесняйтесь обратиться за помощью, введя команду /help в чате с ботом.
