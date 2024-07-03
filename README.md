<p align="center"><img src="https://i.ibb.co/sCb0kRY/IZ-NEWS-bot.jpg" alt="Main-logo" border="0" width="500"></p>

<p align="center">
   <img src="https://img.shields.io/badge/Aiogram-3.7.0-orange)" alt="Aiogram Version">
   <img src="https://img.shields.io/badge/Aiohttp-3.9.5-E86F00" alt="Aiohttp Version">
</p>

<p>Телеграм бот администрирования канала новостей.</p>


## Описание работы бота
Бот является администратором телеграм канала.<br>
Его задача, периодически получать последние новости с ресурса "ИЗВЕСТИЯ IZ" и публиковать в телеграм канале.

<p align="center">
<img src="https://i.ibb.co/5RFsxHT/tg-channel.jpg" alt="Main-logo" border="0" width="250">
<img src="https://i.ibb.co/ygFK86S/tg-bot.jpg" alt="Main-logo" border="0" width="250">
</p>

## Управление ботом:
В чате самого бота реализовано меню управления.
С помощью меню можно выбирать рубрики новостей, которые мы хотим
публиковать в телеграм канале. 


## Установка

Предварительно создайте директорию для приложения (some directory)<br>
Клонируйте код репозитория в созданную директорию (в some directory):
```sh
git clone https://github.com/SwedL/iz_news_bot.git
```
Также в каталоге проекта (some directory) создайте виртуальное окружение, выполнив команду:

- Windows: `python -m venv venv`
- Linux: `python3 -m venv venv`

Активируйте его командой:

- Windows: `.\venv\Scripts\activate`
- Linux: `source venv/bin/activate`


Перейдите в каталог iz_news_bot и установите зависимости в виртуальное окружение:
```sh
cd iz_news_bot
```
```sh
pip install -r requirements.txt
```

Создайте файл `.env` в каталоге
`iz_news_bot/` и положите туда такой код:

```sh
API_TOKEN=ТОКЕН ВАШЕГО ТЕЛЕГРАМ БОТА
CHANNEL_ID=ID ВАШЕГО ТЕЛЕГРАМ КАНАЛА
```

Запустите бота командой:
```sh
python main.py
```
### Тестирование

Проект покрыт различными тестами, которые проверяют его работоспособность.<br>
Тесты запускаются командой:
```sh
python -m core.tests.test_news_source
```
## Автор проекта

* **Осминин Алексей** - [SwedL](https://github.com/SwedL)

