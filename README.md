# <img src="https://thumb.cloud.mail.ru/weblink/thumb/xw1/HWyg/8yyeisuXv" width="400"/>

## Проект "Сервис для компании WanMark"

#### В проекте реализована админка через веб и меню каталога товаров в Telegram боте.
***
#### Реализованы задачи:
* Админка:
  * Структура меню для телеграмм бота.
  * Загрузка фотографий каточкам товара.
  * Настройки почтового сервиса для отправки почты.
  * Принятия заявок от клиентов с отправкой на почту.
  * Рассылка новостей через телеграмм бота.
  * Авторизация.
* Telegram bot:
  * Вывод данных структуры информации из админки.

***
### Прежде чем начать использовать проект нужно:
* Создать бота через [BotFather](https://t.me/BotFather)
* Установить PostgreSQL на сервер или ПК и предварительно настроить БД.
* Установить БД Redis `sudo apt install redis`.
* Создать файл `.evn` для передачи личных данных в Django настройки.
***

    DEBUG=<BOOL>
    SECRET_KEY=<SECRET_KEY>
    POSTGRES_DB=<DB_NAME>
    POSTGRES_USER=<DB_USER>
    POSTGRES_PASSWORD=<DB_PASSWORD>
    DATABASES_HOST=<DB_HOST>
    TOKEN_BOT=<TOKEN_BOT>
    LOG_LEVEL=INFO
    CELERY_BROKER_URL=<redis://xx.xx.xx.xx:6379>
    CELERY_RESULT_BACKEND=<redis://xx.xx.xx.xx:6379>
    CSRF_TRUSTED_ORIGINS=<Доверенные имена указать через ,>


### Разворачивание проекта "Сервис для компании WanMark"


    git clone https://github.com/4byra6ka/WanMark_bot.git
    cd WanMark_bot
    nano env.dev
    poetry install
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver <IP>:<PORT>
    python manage.py run_bot
    celery -A config worker -l INFO


***
### Также можно запустить через Docker:
* Нужно подправить файл `.evn.dev` и поля `EMAIL_HOST_USER`,`EMAIL_HOST_PASSWORD`,`CSRF_TRUSTED_ORIGINS`.
***


    DEBUG=False
    SECRET_KEY=<SECRET_KEY_DJANGO>
    POSTGRES_DB=wanmark_db
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    DATABASES_HOST=wanmark_db
    TOKEN_BOT=<TOKEN_BOT>
    LOG_LEVEL=INFO
    CELERY_BROKER_URL=redis://wanmark_redis:6379/0
    CELERY_RESULT_BACKEND=redis://wanmark_redis:6379/0
    CSRF_TRUSTED_ORIGINS=<CSRF_TRUSTED_ORIGINS>

### Разворачивание проекта "Сервис для компании WanMark" через docker
    git clone https://github.com/4byra6ka/WanMark_bot.git
    cd WanMark_bot
    poetry install
    docker-compose build
    docker-compose up
