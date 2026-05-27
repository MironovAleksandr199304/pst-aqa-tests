# PST AQA Tests

Учебный AQA-проект для практики API и DB automation на Python.

Тестовый стенд:

- UI: https://practicesoftwaretesting.com/
- API: https://api.practicesoftwaretesting.com
- Swagger: https://api.practicesoftwaretesting.com/api/documentation

Для DB-практики используется локальная PostgreSQL, поднятая через Docker Compose.

Цель проекта — постепенно закрепить базовые и прикладные навыки автоматизации: `pytest`, `requests`, contract checks, API client layer, fixtures, `psycopg2`, DB-проверки и дальнейший переход к Playwright.

---

## Стек

Текущий стек:

- Python
- pytest
- requests
- psycopg2
- PostgreSQL
- Docker Compose

Планируемый стек:

- Playwright — для UI-тестов
- Allure — для отчетности
- GitHub Actions — для запуска тестов в CI

---

## Что уже реализовано

Реализовано:

- smoke-проверки публичных GET endpoint'ов;
- проверка HTTP status codes;
- параметризация smoke-тестов через `pytest.mark.parametrize`;
- работа с `response.json()`;
- проверка JSON-структур `dict` и `list`;
- проверка всех элементов списка через `for` и `enumerate`;
- contract checks для `GET /brands`;
- contract checks для `GET /products`;
- nested contract checks для объектов внутри `/products`;
- проверка обязательных полей;
- проверка типов данных;
- проверка непустых строковых значений;
- field-level helpers;
- entity-level helpers;
- nested entity-level helpers;
- API client layer;
- pytest fixtures;
- локальная PostgreSQL через Docker Compose;
- DB client layer через `psycopg2`;
- `fetch_one()` для выборки одной строки;
- `fetch_all()` для выборки нескольких строк;
- `execute_query()` для DDL/DML-запросов с `commit`;
- DB smoke test через `SELECT 1`;
- DB test на несколько строк через `fetch_all`;
- DB test с `CREATE TABLE IF NOT EXISTS`, `TRUNCATE`, `INSERT`, `SELECT WHERE`;
- SQL-параметры через `%s`;
- первый API + DB style test для `/products`;
- второй API + DB style test для `/brands`.

---

## Текущая структура проекта

```text
pst-aqa-tests/
  clients/
    __init__.py
    products_client.py
    brands_client.py

  db/
    __init__.py
    db_client.py
    db_config.py

  helpers/
    __init__.py
    assert_required_string_field.py
    assert_required_number_field.py
    assert_required_bool_field.py
    assert_required_dict_field.py
    assert_required_list_field.py
    assert_brand_contract.py
    assert_product_contract.py
    assert_product_brand_contract.py
    assert_product_category_contract.py
    assert_product_image_contract.py

  tests/
    __init__.py
    test_smoke_get.py
    test_brands_contract.py
    test_brands_contract_all_items.py
    test_products_contract.py
    test_db_connection.py
    test_db_fetch_all.py
    test_db_insert_select.py
    test_api_product_saved_to_db.py
    test_api_brand_saved_to_db.py

  conftest.py
  docker-compose.yml
  requirements.txt
  pytest.ini
  README.md
  .gitignore
```

---

## API client layer

API client layer скрывает прямое использование `requests.get(...)` от тестов.

Реализованы:

```text
ProductsClient
BrandsClient
```

`ProductsClient`:

```text
get_products()
```

`BrandsClient`:

```text
get_brands()
```

Схема:

```text
test
  → fixture
    → api client
      → requests
  → response checks
  → contract checks
```

---

## DB layer

DB layer отвечает за подключение к PostgreSQL и выполнение SQL-запросов.

Реализованы:

```text
db_config.py
db_client.py
```

`db_config.py` возвращает параметры подключения:

```text
host
port
dbname
user
password
```

`DbClient` содержит методы:

```text
get_connection()
fetch_one(query, params=None)
fetch_all(query, params=None)
execute_query(query, params=None)
```

Назначение методов:

```text
fetch_one      → SELECT, одна строка результата
fetch_all      → SELECT, несколько строк результата
execute_query  → CREATE / TRUNCATE / INSERT / UPDATE / DELETE / DROP + commit
```

Схема DB-теста:

```text
test
  → db_client fixture
    → DbClient
      → psycopg2.connect()
      → cursor.execute()
      → fetchone / fetchall / commit
  → assert по результату
```

---

## Pytest fixtures

В `conftest.py` реализованы fixtures:

```text
base_url
product_client
brands_client
db_config
db_client
```

`base_url` хранит базовый адрес API.

`product_client` создает `ProductsClient`.

`brands_client` создает `BrandsClient`.

`db_config` получает конфигурацию подключения к PostgreSQL.

`db_client` создает `DbClient`.

---

## Helper-слой

### Field-level helpers

Field-level helpers проверяют отдельные поля в JSON-объекте.

Реализованы:

```text
assert_required_string_field
assert_required_number_field
assert_required_bool_field
assert_required_dict_field
assert_required_list_field
```

Они проверяют:

```text
поле существует
значение имеет ожидаемый тип
строковое значение не пустое
```

Для числовых полей учитывается особенность Python: `bool` является наследником `int`, поэтому `True` и `False` не должны проходить как валидное числовое значение.

---

### Entity-level helpers

Реализованы:

```text
assert_brand_contract
assert_product_contract
assert_product_brand_contract
assert_product_category_contract
assert_product_image_contract
```

`assert_brand_contract` проверяет объект `brand` из ответа `/brands`:

```text
id    string
name  string
slug  string
```

`assert_product_contract` проверяет объект `product` из ответа `/products`:

```text
id                  string
name                string
description         string
price               number
is_location_offer   bool
is_rental           bool
co2_rating          string
in_stock            bool
is_eco_friendly     bool
product_image       dict + internal contract
category            dict + internal contract
brand               dict + internal contract
```

`assert_product_brand_contract` проверяет вложенный объект `brand` внутри `/products`:

```text
id    string
name  string
```

Важно: это не тот же contract shape, что у `/brands`, потому что внутри `/products.brand` нет поля `slug`.

`assert_product_category_contract` проверяет вложенный объект `category` внутри `/products`:

```text
id    string
name  string
slug  string
```

`assert_product_image_contract` проверяет вложенный объект `product_image` внутри `/products`:

```text
id           string
by_name      string
by_url       string
source_name  string
source_url   string
file_name    string
title        string
```

---

## Проверяемые endpoint'ы

### GET /brands

Проверяется:

```text
response является list
список не пустой
каждый элемент списка является brand object
у каждого brand есть id, name, slug
id/name/slug являются строками
id/name/slug не пустые
```

Схема теста:

```text
test_brands_contract_all_items
  → brands_client fixture
  → BrandsClient.get_brands()
  → assert_brand_contract
```

---

### GET /products

Проверяется:

```text
response является dict
response["data"] существует
response["data"] является list
response["data"] не пустой
каждый элемент response["data"] является product object
каждый product соответствует product contract
каждый product содержит валидные вложенные объекты product_image, category и brand
```

Схема теста:

```text
test_products_contract_all_items
  → product_client fixture
  → ProductsClient.get_products()
  → assert_product_contract
```

---

## DB-проверки

### test_db_connection

Проверяет базовое подключение к PostgreSQL и выполнение простого запроса:

```text
SELECT 1
```

Ожидаемый результат:

```text
(1,)
```

---

### test_db_fetch_all

Проверяет работу `fetch_all()` на запросе, который возвращает несколько строк.

Ожидаемый результат по смыслу:

```text
[(1,), (2,)]
```

---

### test_db_insert_select

Проверяет базовый сценарий работы с таблицей:

```text
CREATE TABLE IF NOT EXISTS
TRUNCATE TABLE
INSERT с параметрами
SELECT WHERE с параметром
assert по данным из БД
```

Проверяется, что после вставки запись реально доступна через `SELECT`.

---

## API + DB style tests

Эти тесты закрепляют паттерн:

```text
API response
  → данные из ответа
  → INSERT в локальную PostgreSQL
  → SELECT из БД
  → сравнение API data и DB data
```

Важно: это учебный API + DB style pattern. Локальная PostgreSQL не является реальной БД сервиса Practice Software Testing.

### test_api_product_saved_to_db

Сценарий:

```text
GET /products
взять первый product из response["data"]
создать таблицу test_products
очистить таблицу
вставить id, name, price
сделать SELECT по id
сравнить данные из БД с API response
```

### test_api_brand_saved_to_db

Сценарий:

```text
GET /brands
взять первый brand из response
создать таблицу test_brands
очистить таблицу
вставить id, name, slug
сделать SELECT по id
сравнить данные из БД с API response
```

---

## Установка и запуск

Клонировать репозиторий:

```bash
git clone https://github.com/MironovAleksandr199304/pst-aqa-tests.git
cd pst-aqa-tests
```

Создать виртуальное окружение:

```bash
python -m venv .venv
```

Активировать виртуальное окружение на Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Активировать виртуальное окружение на Windows CMD:

```cmd
.venv\Scripts\activate.bat
```

Активировать виртуальное окружение на Linux / macOS:

```bash
source .venv/bin/activate
```

Установить зависимости:

```bash
pip install -r requirements.txt
```

Поднять PostgreSQL через Docker Compose:

```bash
docker compose up -d
```

Проверить запущенные контейнеры:

```bash
docker ps
```

Запустить все тесты:

```bash
pytest
```

Запустить тесты с подробным выводом:

```bash
pytest -s -v
```

Запустить контрактные проверки `/brands`:

```bash
pytest tests/test_brands_contract_all_items.py -s -v
```

Запустить контрактные проверки `/products`:

```bash
pytest tests/test_products_contract.py -s -v
```

Запустить DB smoke test:

```bash
pytest tests/test_db_connection.py -s -v
```

Запустить DB test на `fetch_all`:

```bash
pytest tests/test_db_fetch_all.py -s -v
```

Запустить DB test на `INSERT` / `SELECT`:

```bash
pytest tests/test_db_insert_select.py -s -v
```

Запустить API + DB style test для `/products`:

```bash
pytest tests/test_api_product_saved_to_db.py -s -v
```

Запустить API + DB style test для `/brands`:

```bash
pytest tests/test_api_brand_saved_to_db.py -s -v
```

---

## Текущий фокус обучения

Сейчас проект используется для закрепления навыков API и DB automation:

- работа с `requests`;
- запуск тестов через `pytest`;
- проверка `status_code`;
- работа с `response.json()`;
- проверка `dict` / `list`;
- проверка обязательных полей;
- проверка типов данных;
- проверка непустых значений;
- проверка всех элементов списка через `for` и `enumerate`;
- вынос повторяющихся проверок в helper-функции;
- проверка вложенных JSON-объектов через nested contract helpers;
- вынос HTTP-запросов в API client layer;
- использование pytest fixtures;
- подключение к PostgreSQL через `psycopg2`;
- выполнение `SELECT` через `fetch_one` и `fetch_all`;
- выполнение DDL/DML-запросов через `execute_query`;
- использование `commit` для запросов, меняющих состояние БД;
- использование параметров SQL-запроса через `%s`;
- связывание API response и DB-проверок в одном тесте.

---

## Roadmap

### 1. Добить вложенные contracts для `/products`

Статус: выполнено.

Реализованы:

```text
assert_product_brand_contract
assert_product_category_contract
assert_product_image_contract
```

---

### 2. Сделать API client layer

Статус: выполнено базово.

Реализованы:

```text
ProductsClient
BrandsClient
```

---

### 3. Ввести pytest fixtures

Статус: выполнено базово.

Реализованы:

```text
base_url
product_client
brands_client
db_config
db_client
```

---

### 4. Начать psycopg2

Статус: выполнено базово.

Реализовано:

```text
подключение к БД
SELECT
fetch_one
fetch_all
execute_query
CREATE TABLE IF NOT EXISTS
TRUNCATE
INSERT
SELECT WHERE
параметры SQL-запроса
```

---

### 5. Сделать первый API + DB style test

Статус: выполнено базово.

Реализованы:

```text
test_api_product_saved_to_db
test_api_brand_saved_to_db
```

---

### 6. Negative API tests

Статус: следующий этап.

План:

```text
добавить методы get_product_by_id / get_brand_by_id при необходимости
проверить несуществующий id
проверить ожидаемый 4xx status code
проверить body ошибки, если он есть
```

---

### 7. POST-сценарии

Статус: после negative tests.

План:

```text
найти подходящий POST endpoint
разобрать payload
добавить метод в client
отправить POST-запрос
проверить status code и response body
```

---

### 8. Playwright

Статус: после API/DB базы и базовых negative/POST API tests.

После закрепления API/DB базы перейти к UI:

```text
открыть страницу
найти элемент
кликнуть
проверить текст
ввести Page Object
```

---

## Важное замечание

Это учебный проект, а не production-ready framework.

Код развивается постепенно: сначала простые тесты и ручное закрепление базовых конструкций, затем рефакторинг, выделение повторяющейся логики и построение более полноценной структуры автотестов.

README подготовлен с помощью ChatGPT и отредактирован вручную.

Код тестов пишется самостоятельно в рамках обучения. ChatGPT используется как ментор для объяснения теории, ревью решений и разбора ошибок.
