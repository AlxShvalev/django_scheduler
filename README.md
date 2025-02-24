# Проект file_scheduler

### Назначение:
Проект предназначен для чтения файлов `*.xlsx` 
в локальной директории и сохранения их в базе данных

### Описание функционала интерфейса:
1. Сервис каждую минуту сканирует локальную директорию 
на наличие файлов `*.xslx`.
2.  В случае нахождения одного или нескольких файлов сервис загружает
содержимое файла в таблицу в базе данных.
3. Для каждого нового файла создается новая таблица.
4. Наименование таблицы генерируется из имени файла с заменой
не буквенно-цифровых символов на символ `_` и приведения к нижнему регистру.
5. При обработке содержимого файла, столбцы, которые могут быть преобразованы 
к типу `datetime`, преобразовываются к типу `datetime`
6. События обработки пишутся в файл `logs/celery.log` и в консоль контейнера `celery`

    - Файл не является `*.xlsx` файлом;
    - Файл `*.xlsx` не может быть прочитан;
    - При записи содержимого в базу данных произошла ошибка;
    - Файл успешно обработан.

7. После успешной записи содержимого файла в базу данных, файл удаляется из директории

### Запуск
Для запуска проекта необходимо заполнить файл `.env.template`

- `SECRET_KEY` - секретный ключ для приложения django
- `PORT` - Порт для запуска Django-приложения
- `REDIS_PORT` - Порт для запуска контейнера Redis
- `FILES_LOCATION` - Путь для поиска файлов `*.xlsx`. Может быть абсолютным 
или относительным. Относительный путь должен начинаться с `./`

Переименовать файл `.env.template` в `.env`.

Для разворачивания и запуска сервиса используется `docker-compose`. 
Из директории проекта (директория с файлом `docker-compose.yml`)
выполнить команду:

```bash
    docker compose up -d --build
```

### Технологии

1. Сервис работает на `django`.
2. Для запуска задач по расписанию используются `celery` и `celery-beat`
3. В качестве брокера сообщений для Celery используется `redis`
4. Для чтения файлов, обработки и сохранения в базу данных используется библиотека `pandas`
5. Для удобства разворачивания и запуска сервиса использован `docker-compose`
6. В качестве СУБД выбрана `SQLite`, т.к. этот вариант был проще и быстрее при разработке 
и специфичных требований к СУБД не предъявлялось.

### Автор
Алексей Швалёв
