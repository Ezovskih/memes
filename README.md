# «Коллекция мемов»

## Описание
Микросервис для работы с коллекцией мемов.

Используется FastAPI для обработки запросов и MinIO для хранения изображений.

## Подготовка Windows-сервера
По причине разработки под Windows и отсутствия рабочего Linux-сервера, предлагается инструкция под ОС Windows.
> Прилагаемый docker-compose.yml не тестировался и прилагается как образец для разработки под Linux.

### I. СУБД
1. [Скачайте](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads) и установите последнюю версию СУБД PostgreSQL:

> В процессе разработки использовалась версия PostgreSQL 17.2.

2. Создайте базу данных meme_db:
```pgsql
-- DROP DATABASE IF EXISTS meme_db;

CREATE DATABASE meme_db WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Russian_Russia.1251'
    LC_CTYPE = 'Russian_Russia.1251'
    LOCALE_PROVIDER = 'libc'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;
```
3. Создайте (роль) пользователя "meme_user" с паролем "12345678" (или другим):
```pgsql
-- DROP ROLE IF EXISTS meme_user;

CREATE ROLE meme_user WITH
    LOGIN
    NOSUPERUSER
    INHERIT
    NOCREATEDB
    NOCREATEROLE
    NOREPLICATION
    NOBYPASSRLS
    PASSWORD '12345678';
```
> Таблицы создаются автоматически при инициализации приложения.

### II. Система хранения файлов
1. [Скачайте](https://dl.min.io/server/minio/release/windows-amd64/minio.exe) и скопируйте в любой каталог последнюю версию исполняемого файла системы хранения MinIO:
> В процессе разработки использовалась версия MinIO 1.23.4.

2. Создайте каталог для хранения изображений (хранилище) на диске с достаточным объемом свободного пространства.


3. Запустите сервер выполнив в консоли команду:
```console
[путь к файу]\minio.exe server [путь к хранилищу] --console-address :9001
```
> **ВАЖНО!** Не закрывайте окно консоли во время работы сервиса.
4. Войдите в "консоль" хранилища по адресу http://127.0.0.1:9001 с логином и паролем: `minioadmin`, затем создайте ключ доступа `minio`:`12345678` (или другой) и bucket-хранилище "`images`".

### III. Установка и настройка сервера API
1. [Скачайте](https://www.python.org/downloads/) и установите Python 3, если он еще не установлен.
> Разработка велась с использованием Python 3.12.

2. Выполните клонирование репозитория и войдите в рабочий каталог:
```console
git clone https://github.com/Ezovskih/memes.git
cd memes
```
3. Создайте и активируйте виртуальную среду: 
```console
python -m venv env
./.venv/Scripts/Activate.bat
```
4. Установите необходимые библиотеки и модули:
```console
pip install -r requirements.txt
```
5. Проверьте настройки подключения (адреса, порты и пароли) к подсистемам в файле `app/config.py`.


6. Запустите сервер выполнив с консоли команду: 
```console
python main.py
```

**или** (для динамической перезагрузки при наличии изменений в коде):

```console
uvicorn main:app --reload
```

## Публичное API
![API](/api.png)
- `GET /memes`: Получить список всех мемов.
- `GET /memes/{id}`: Получить мем по идентификатору.
- `POST /memes`: Добавить новый мем.
- `PUT /memes/{id}`: Обновить или заменить мем.
- `DELETE /memes/{id}`: Удалить мем.

Документация к точкам доступа доступна по адресу:
http://127.0.0.1:8080/docs
