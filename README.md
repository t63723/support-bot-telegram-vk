# Простой бот технической поддержки для telegram.org и vk.com
Поддерживает общение на естественном языке с помощью dialogflow.com

Для работы нужно создать проект на dialogflow

## Установка и запуск
### Определение переменных окружения для работы
В папке с файлами нужно создать файл '.env' в котором заполнить значение переменных окружения.

Описание содержания файла `.env`

```
MONITORING_CHAT_ID=<ваш chatid в телеграм>
MONITORING_TOKEN=<токен бота для мониторинга ошибок>

TELEGRAM_TOKEN=<токен основного бота для телеграм>
VK=<токен группы вконтакте>

PROJECT_ID=<имя проекта на dialogflow.com>
GA-KEY-CLIENT=<имя файла с ключами для подключения бота к dialogflow.com>
GA-KEY-ADMIN=<имя файла с ключами для обучения бота>
```

### Запуск
```
$ pip install -r requirements.txt
```

telegram bot:
```
$ python telegram_support_bot.py
```

vk bot:
```
$ python vk_support_bot.py
```

### Обучение
Бот может быть обучен (файл для обучения 
[ссылка на пример](https://dvmn.org/media/filer_public/a7/db/a7db66c0-1259-4dac-9726-2d1fa9c44f20/questions.json))

```sh
$ python train_support_bot.py --url <file_url>
```

### Попробовать
[vk](https://t.me/katsupko_support_bot)  
[telegram](https://vk.com/public183309808)

### Пример работы
![gif](https://i.ibb.co/5F5XDyd/ezgif-com-video-to-gif-1.gif)