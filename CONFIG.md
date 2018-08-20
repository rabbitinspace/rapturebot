# Настройка конфига

Конфиг находится в файле `config.json`. 

Вам нужно создать его самостоятельно. Пример конфига находится в файле `config.example.json`. Копируйте его в файл `config.json` и приступайте к настройке.

Условимся, что `--` перед названием настройки означает, что она отключена. Вообще, бот смотрит только названия известных ему параметров, все остальные он игнорирует.

## Основные параметры бота

Без них бот не заработает.

### bot_token

Токен бота. В телеграме пишите [@botfather](https://t-do.ru/botfather), вводите команду `/newbot`, далее любые имена и в итоге он выдаст токен бота. Его и пишем сюда.

Не забудьте зайти в настройки бота. Разрешить ему группы. И отключить privacy mode.

### database

В базе хранятся имена пользователей, а они любят вставлять туда эмодзи. Для корректного отображения нужно [изменить настройки бд для поддержки utf8mb4](https://mathiasbynens.be/notes/mysql-utf8mb4#character-sets). И перезапустить бд.

Создайте новую базу данных, например `rapturebot` (сравнение выбрать utf8mb4_general_ci). Укажите юзера и пароль для доступа к ней (если пароля нет, то просто удалите его из строки, будет что-то вроде `root:@localhost`).

Создайте таблицы при помощи [rapturebot_empty.sql](https://gist.github.com/pongo/deb687edcbc49962ca8e1e58a4b4bfd4).

### webhook_domain

По-умолчанию этот параметр отключен через `--`. 

Если параметр отключен, то бот будет работать через лонгполлинг. Если параметр включить (убрать `--`) и указать правильный домен, то бот начнет работать через вебхуки. Отмечу, что если в стране заблокирован телеграм, то вебхуки, скорее всего, не заработают.

На сервере домен можно узнать командой:

```console
$ hostname -f
domain.example.com
```

Помимо указания домена, нужно создать самоподписанный сертификат и расположить файлы `private.key` и `cert.pem` рядом с файлом `config.json`.

[Подробнее про вебхуки и создание сертификата](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks#a-ssl-certificate).

### cache

Параметры работы с редисом. Скорее всего, все заработает со значениями по-умолчанию.

### logging

Параметры логирования. Тоже достаточно стандартных. Можно **level** поменять на `DEBUG` и офигеть.

### telegram_proxy

Если нужно работать через прокси, то включите параметр и укажите нужные значения.

## Параметры чатов

### admins_ids

Админы чата считаются так же админами бота в этом чате. Но можно указать здесь uid людей, которые всегда будут админами бота. Укажите свой. 

Свой userid можно узнать через бота [@userinfobot](https://t-do.ru/userinfobot).

### debug_uid

На этот uid бот будет посылать отладочные сообщения в некоторых случаях. Укажите свой.

### weekly_stats_chats_ids

ID чатов, в которых бот автоматически постит стату за прошедшую неделю (постится в полночь понедельника по Москве). ID чатов начинаются с минуса. 

Отмечу, что сама стата собирается независимо от наличия или отсутствия чата в этом параметре.

### chats

Бот работает только в указанных чатах.

Чтобы узнать id чата: запустите бота, добавьте его в чат, напишите что-нибудь. В логах бота появится строка `Chat -198791234 not in config`. Id этого чата: -198791234. Копируйте в конфиг и настраиваете, какие команды будут работать в этом чате.

Простейший вариант выглядит так:

```json
"chats": {
  "-198791234": {
    "all_cmd": true
  }
}
```

Как видите, у каждого чата есть собственные настройки:

| Параметр чата     | Описание
| :---              | :---
| all_cmd           | Если `true`, то все команды включены, кроме отключенных через `disabled_commands`. <br>Если `false`, то включены будут только указанные в параметре `enabled_commands`. 
| comment           | Пояснение, что это за канал. Ни на что не влияет, просто для удобства.
| enabled_commands  | Список включенных в чате команд. Нужен только если `all_cmd=false`. Список большинства команд находится в файле `commands` в корне проекта. 
| disabled_commands | Список отключенных команд. Нужен только если `all_cmd=true`, но какие-то команды хочется отключить.
| commands_config   | У некоторых команд есть настройки, уникальные для конкретного чата.

Настройки **commands_config**:

| Команда | Настройка | Описание
| :---    | :---      | :---
| time    | sort      | Команда `/time` по-умолчанию сортирует города по времени. Если здесь указать `false`, то они будут отсортированы как в конфиге для команды /`time`. 
| welcome | text      | Когда человека добавляют в чат, то бот напишет этот текст в канал. Через `{username}` можно указать юзернейм новичка. 

## Параметры команд

### off_delay

Количество секунд, на которое отключаются команды через `/off`. По-умолчанию 5 минут (300 сек).

### top_users_num

Количество строк в команде `/stat`.

---

TODO: доделать
