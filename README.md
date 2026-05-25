# PST AQA Tests

Учебный AQA-проект для практики автоматизации тестирования API на Python.

В качестве тестового стенда используется Practice Software Testing:

- UI: https://practicesoftwaretesting.com/
- API: https://api.practicesoftwaretesting.com
- Swagger: https://api.practicesoftwaretesting.com/api/documentation

Цель проекта — постепенно отработать базовые и прикладные навыки API automation: от простых `requests`-тестов до более структурированного проекта с client layer, fixtures, DB-проверками и дальнейшим переходом к UI-автоматизации.

---

## Стек

На текущем этапе используется:

- Python
- pytest
- requests

Планируемый стек по мере развития проекта:

- psycopg2 — для проверок БД;
- Playwright — для UI-тестов;
- Allure — для отчетности;
- GitHub Actions — для запуска тестов в CI.

---

## Что уже реализовано

На текущем этапе реализованы базовые API-тесты, contract checks для `/brands` и `/products`, вложенные contract checks для объектов внутри `/products`, а также первый вариант API client layer.

Реализовано:

- smoke-проверки публичных GET endpoint'ов;
- проверка ожидаемых HTTP status codes;
- параметризация smoke-тестов через `pytest.mark.parametrize`;
- работа с `response.json()`;
- проверка JSON-структур `dict` и `list`;
- проверка всех элементов списка через `for` и `enumerate`;
- контрактная проверка `GET /brands`;
- контрактная проверка `GET /products`;
- проверка обязательных полей;
- проверка типов данных;
- проверка непустых строковых значений;
- вынос повторяющихся assert'ов в helper-функции;
- разделение проверок на:
  - field-level helpers;
  - entity-level helpers;
  - nested entity-level helpers;
  - endpoint-level tests;
- вложенные contract helpers для объектов внутри `/products`:
  - `product_image`;
  - `category`;
  - `product_brand`;
- API client layer для основных ресурсов:
  - `ProductsClient`;
  - `BrandsClient`.

---

## Текущая структура проекта

```text
pst-aqa-tests/
  clients/
    __init__.py
    products_client.py
    brands_client.py

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

  requirements.txt
  pytest.ini
  README.md
  .gitignore
```

---

## Client layer

В проект добавлен первый API client layer.

Client layer отвечает за отправку HTTP-запросов и скрывает прямое использование `requests.get(...)` от тестов.

Реализованы:

```text
ProductsClient
BrandsClient
```

`ProductsClient` умеет получать список продуктов:

```text
get_products()
```

`BrandsClient` умеет получать список брендов:

```text
get_brands()
```

До client layer тесты напрямую вызывали `requests.get(...)`.

После добавления client layer тесты используют клиент:

```text
test
  → client.get_products()
  → response checks
  → contract checks
```

Это позволяет разделить ответственность:

```text
test        → сценарий и проверки
client      → HTTP-запросы
helpers     → contract/assertion checks
```

---

## Helper-слой

В проекте есть набор универсальных проверок и contract-helper'ов.

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

Для числовых полей отдельно учитывается особенность Python: `bool` является наследником `int`, поэтому `True` и `False` не должны проходить как валидное числовое значение.

---

### Entity-level helpers

Entity-level helpers проверяют структуру конкретной сущности.

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
product_image       dict + внутренний contract
category            dict + внутренний contract
brand               dict + внутренний contract
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

Тест использует `BrandsClient`:

```text
test_brands_contract_all_items
  → BrandsClient.get_brands()
  → assert_brand_contract
```

---

### GET /products

Проверяется структура paginated/object response:

```text
response является dict
response["data"] существует
response["data"] является list
response["data"] не пустой
каждый элемент response["data"] является product object
каждый product соответствует product contract
каждый product содержит валидные вложенные объекты product_image, category и brand
```

Текущая модель:

```text
/products
response → dict
response["data"] → list
product → dict
  product_image → dict
  category → dict
  brand → dict
```

Тест использует `ProductsClient`:

```text
test_products_contract_all_items
  → ProductsClient.get_products()
  → assert_product_contract
```

Контрактная проверка `/products` успешно проходит:

```text
tests/test_products_contract.py::test_products_contract_all_items PASSED
```

Контрактная проверка `/brands` успешно проходит:

```text
tests/test_brands_contract_all_items.py::test_brands_contract_all_items PASSED
```

---

## Архитектурный подход

Проект строится по принципу разделения ответственности.

Тест отвечает за сценарий:

```text
создать API client
получить response через client method
проверить status_code
проверить верхнюю структуру ответа
для каждого объекта вызвать contract-check
```

Client отвечает за HTTP-запросы:

```text
ProductsClient
BrandsClient
```

Entity-helper отвечает за структуру конкретной сущности:

```text
brand
product
product_brand
category
product_image
```

Field-helper отвечает за атомарную проверку конкретного поля:

```text
поле существует
поле имеет нужный тип
поле не пустое, если это обязательная строка
```

Общая схема:

```text
test
  → api client
    → requests
  → entity-helper
    → nested entity-helper
      → field-helper
```

Пример для `/products`:

```text
test_products_contract_all_items
  → ProductsClient.get_products()
  → assert_product_contract
    → assert_required_string_field
    → assert_required_number_field
    → assert_required_bool_field
    → assert_required_dict_field
    → assert_product_image_contract
      → assert_required_string_field
    → assert_product_category_contract
      → assert_required_string_field
    → assert_product_brand_contract
      → assert_required_string_field
```

Такой подход позволяет держать тесты читаемыми, а повторяющуюся логику запросов и проверок — переиспользуемой.

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

Запустить все тесты:

```bash
pytest
```

Запустить тесты с подробным выводом:

```bash
pytest -s -v
```

Запустить конкретный файл:

```bash
pytest tests/test_smoke_get.py -s -v
```

Запустить контрактные проверки `/brands`:

```bash
pytest tests/test_brands_contract_all_items.py -s -v
```

Запустить контрактные проверки `/products`:

```bash
pytest tests/test_products_contract.py -s -v
```

---

## Текущий фокус обучения

Сейчас проект используется для закрепления навыков API automation:

- работа с `requests`;
- запуск тестов через `pytest`;
- проверка `status_code`;
- работа с `response.json()`;
- проверка `dict` / `list`;
- проверка обязательных полей;
- проверка типов данных;
- проверка непустых значений;
- параметризация тестов;
- проверка всех элементов списка через `for` и `enumerate`;
- диагностика падений через сообщения в `assert`;
- вынос повторяющихся проверок в helper-функции;
- проверка вложенных JSON-объектов через nested contract helpers;
- вынос HTTP-запросов в API client layer;
- разделение тестовой логики на уровни:
  - test;
  - api client;
  - entity-helper;
  - nested entity-helper;
  - field-helper.

---

## Roadmap

Дальнейшее обучение ведется по следующему порядку.

### 1. Добить вложенные contracts для `/products`

Статус: выполнено.

Реализованы helper'ы:

```text
assert_product_brand_contract
assert_product_category_contract
assert_product_image_contract
```

Цель этапа была в том, чтобы начать проверять не только наличие вложенных объектов, но и их внутреннюю структуру.

---

### 2. Сделать API client layer

Статус: базово выполнено.

Реализованы классы:

```text
ProductsClient
BrandsClient
```

Цель этапа была в том, чтобы убрать прямые `requests.get(...)` из основных contract-тестов и вынести работу с API в отдельный слой.

Текущая схема:

```text
test
  → api client
    → requests
  → contract helper
```

---

### 3. Ввести pytest fixtures

Статус: следующий этап.

Планируемые fixtures:

```text
base_url
products_client
brands_client
test data
```

Цель — убрать дублирование настроек и подготовить проект к расширению.

---

### 4. Начать psycopg2

Статус: после fixtures.

План:

```text
подключение к БД
SELECT
проверка одной записи
helper для fetch_one / fetch_all
```

---

### 5. Сделать первый API + DB test

Статус: после базового psycopg2.

Целевая структура теста:

```text
отправить API-запрос
проверить response
проверить данные в БД
```

---

### 6. Только потом Playwright

Статус: после API/DB базы.

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
