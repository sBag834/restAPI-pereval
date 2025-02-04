# REST API для управления перевалами

## Описание проекта

Этот проект представляет собой REST API для управления данными о перевалах. Он позволяет пользователям добавлять, редактировать и получать информацию о перевалах, а также управлять статусом модерации. API разработан с использованием Flask и PostgreSQL.

## Задача

Основная задача заключалась в создании API, который позволяет:

- Добавлять новые записи о перевалах.
- Получать информацию о конкретном перевале по его ID.
- Редактировать существующие записи, если они находятся в статусе `new`.
- Получать список всех перевалов, отправленных пользователем с определённым адресом электронной почты.

## Технологии

- **Flask**: веб-фреймворк для создания RESTful API.
- **PostgreSQL**: реляционная база данных для хранения информации о перевалах.
- **psycopg2**: библиотека для взаимодействия с PostgreSQL из Python.
- **dotenv**: библиотека для работы с переменными окружения.

## Установка

1. Клонируйте репозиторий:\
`git clone https://github.com/sBag834/restAPI-pereval` \
`cd restAPI-pereval`


2. Установите зависимости:\
`pip install -r requirements.txt`


3. Создайте файл `.env` в корневом каталоге проекта и добавьте параметры подключения к базе данных: 


`FSTR_DB_HOST=localhost`\
`FSTR_DB_PORT=5432`\
`FSTR_DB_LOGIN=ваш_логин`\
`FSTR_DB_PASS=ваш_пароль`


4. Запустите приложение:\
`python app.py`

## Использование API

### 1. Добавление нового перевала

**POST /submitData**

**Тело запроса (JSON):**

    {
    "date_added": "2025-01-08T17:50:00",
    "raw_data": "{\"beautyTitle\": \"пер.\", \"title\": \"Новый перевал\", \"user\": {\"email\": \"meoww@gmail.com\"}}",
    "images": "{\"images\": [{\"id\": 56, \"title\":\"Изображение\"}]}"
    }

**Ответ:**

    {
    "message": "Data submitted successfully",
    "id": 1
    }

### 2. Получение перевала по ID

**GET /submitData/id**

**Пример запроса:**

GET `http://localhost:5000/submitData/1`

**Ответ:**

    {
    "id": 1,
    "date_added": "2025-01-02T14:00:00",
    "raw_data": {...},
    "images": {...},
    "status": "new"
    }

### 3. Редактирование перевала

**PATCH /submitData/id**

**Тело запроса (JSON):**

    {
    "date_added": "2025-01-08T17:50:00",
    "raw_data": "{\"beautyTitle\": \"пер.\", \"title\": \"Обновлённый перевал\", \"user\": {\"email\": \"meoww@gmail.com\"}}",
    "images": "{\"images\": [{\"id\": 56, \"title\":\"Обнавлённое изображение\"}]}"
    }

**Ответ:**

    {
    "state": 1,
    "message": "Record updated successfully."
    }

### 4. Получение всех перевалов пользователя по email

**GET /submitData/?user__email=<email>**

**Пример запроса:**

GET `http://localhost:5000/submitData/?user__email=user@email.tld`

**Ответ:**

    [
    {
    "id": 1,
    ...
    },
    {
    "id": 2,
    ...
    }
    ]

## Использование Tests

1. В директории `tests`, в файле `test_database.py`, подставте свои данные для доступа к БД
2. Запустите приложение:\
`python app.py`
3. В отдельном терминале запустите тесты\
`python -m unittest discover tests/`
