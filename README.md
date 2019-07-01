# Простой бот технической поддержки для telegram.org и vk.com
Поддерживает общение на естественном языке с помощью dialogflow.com

Для работы нужно создать проект на dialogflow

## Установка и запуск
### Определение переменных окружения для работы
В папке с файлами нужно создать файл '.env' в котором заполнить значение переменных окружения.

Описание содержания файла `.env`

```
monitoring_chat_id=<ваш chatid в телеграм>
monitoring_token=<токен бота для мониторинга ошибок>

telegram_token=<токен основного бота для телеграм>
vk=<токен группы вконтакте>

project_id=<имя проекта на dialogflow.com>
ga-key-client=<имя файла с ключами для подключения бота к dialogflow.com>
ga-key-admin=<имя файла с ключами для обучения бота>
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
Бот может быть обучен (файла для обучения 
[ссылка на пример](https://dvmn.org/media/filer_public/a7/db/a7db66c0-1259-4dac-9726-2d1fa9c44f20/questions.json))
```
$ python train_support_bot.py
```

### Попробовать
[vk](https://t.me/katsupko_support_bot)  
[telegram](https://vk.com/public183309808)

### Пример работы
![gif](https://i.ibb.co/5F5XDyd/ezgif-com-video-to-gif-1.gif)