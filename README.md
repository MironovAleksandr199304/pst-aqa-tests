# PST AQA Tests

Учебный AQA-проект для практики автоматизации тестирования на Python.

В качестве тестового стенда используется Practice Software Testing:

- UI: https://practicesoftwaretesting.com/
- API: https://api.practicesoftwaretesting.com
- Swagger: https://api.practicesoftwaretesting.com/api/documentation

Цель проекта — постепенно собрать понятный automation framework для тестирования API, UI и интеграций с БД.

---

## Стек

На текущем этапе используется:

- Python
- pytest
- requests

Планируемый стек по мере развития проекта:

- Playwright — для UI-тестов
- psycopg2 — для проверок БД
- jsonschema / pydantic — для контрактных проверок
- Allure — для отчетности
- GitHub Actions — для запуска тестов в CI
- pytest-asyncio / async Python — для изучения асинхронного тестирования
- gRPC — для практики тестирования RPC-сервисов
- Locust / k6 — для базового нагрузочного тестирования

---

## Что уже реализовано

На текущем этапе проект содержит первые API-тесты и начальный слой helper-функций.

Реализовано:

- smoke-проверки публичных GET endpoint'ов;
- проверка ожидаемых HTTP status codes;
- параметризация smoke-тестов через `pytest.mark.parametrize`;
- первая контрактная проверка ответа `GET /brands`;
- проверка структуры JSON-ответа;
- проверка, что response является `list`;
- проверка, что список не пустой;
- проверка всех объектов в списке через `for` и `enumerate`;
- проверка обязательных полей;
- проверка типов данных;
- проверка непустых значений;
- вынос повторяющихся assert'ов в helper-функции;
- разделение проверок на field-level helper и entity-level helper.

Пример проверяемой логики:

```text
GET /brands
→ status code 200
→ response является list
→ список не пустой
→ каждый элемент списка является brand object
→ у каждого brand есть поля id, name, slug
→ поля id, name, slug имеют тип str
→ поля id, name, slug не пустые
Текущая структура проекта
pst-aqa-tests/
  helpers/
    __init__.py
    assert_required_string_field.py
    assert_brand_contract.py

  tests/
    test_smoke_get.py
    test_brands_contract.py
    test_brands_contract_all_items.py

  requirements.txt
  pytest.ini
  README.md
  .gitignore
Helper-слой

В проекте появился первый слой переиспользуемых проверок.

Field-level helper

assert_required_string_field проверяет одно обязательное строковое поле:

поле существует
поле имеет тип str
поле не пустое

Этот helper не знает ничего о конкретной ручке или сущности. Он универсальный и может использоваться для разных объектов.

Entity-level helper

assert_brand_contract проверяет структуру объекта brand:

brand содержит id
brand содержит name
brand содержит slug
id/name/slug являются строками
id/name/slug не пустые

Внутри assert_brand_contract используется универсальный helper assert_required_string_field.

Такой подход позволяет держать тесты более читаемыми: тест описывает сценарий, а детали проверки структуры вынесены в helper-функции.

Пример архитектурного подхода

Тест отвечает за сценарий:

GET /brands должен вернуть непустой список брендов,
и каждый бренд должен соответствовать контракту brand.

Entity-helper отвечает за структуру конкретной сущности:

brand должен содержать id, name, slug.

Field-helper отвечает за атомарную проверку поля:

обязательное строковое поле должно существовать,
быть строкой и быть непустым.
Установка и запуск

Клонировать репозиторий:

git clone https://github.com/MironovAleksandr199304/pst-aqa-tests.git
cd pst-aqa-tests

Создать виртуальное окружение:

python -m venv .venv

Активировать виртуальное окружение на Windows:

.venv\Scripts\activate

Установить зависимости:

pip install -r requirements.txt

Запустить все тесты:

pytest

Запустить тесты с подробным выводом:

pytest -s -v

Запустить конкретный файл:

pytest tests/test_smoke_get.py -s -v

Запустить контрактную проверку /brands:

pytest tests/test_brands_contract_all_items.py -s -v
Текущий фокус обучения

Сейчас проект используется для закрепления базовых навыков API automation:

работа с requests;
запуск тестов через pytest;
проверка status_code;
работа с response.json();
проверка dict / list;
проверка обязательных полей;
проверка типов данных;
проверка непустых значений;
параметризация тестов через pytest.mark.parametrize;
проверка всех элементов списка через for и enumerate;
диагностика падений через сообщения в assert;
вынос повторяющихся проверок в helper-функции;
разделение тестовой логики на уровни: test → entity-helper → field-helper.
Roadmap

Ближайшие шаги:

добавить контрактные проверки для /products;
проверить вложенные объекты brand, category, product_image;
добавить helper для обязательных числовых полей;
добавить helper для обязательных boolean-полей;
добавить helper для проверки вложенных dict-объектов;
привести smoke-тесты и contract-тесты к единому стилю;
добавить API client layer;
добавить fixtures;
добавить негативные API-тесты;
добавить авторизацию;
добавить тестовые данные и data builders;
добавить проверки БД через psycopg2;
добавить UI-тесты на Playwright;
добавить Allure-отчеты;
настроить запуск в GitHub Actions.

Дальнейшие направления развития:

async Python;
pytest-asyncio;
gRPC-тесты;
базовое нагрузочное тестирование;
работа с flaky tests;
подготовка тестовых данных через вспомогательные сервисы/утилиты.
Важное замечание

Это учебный проект, а не production-ready framework.

Код развивается постепенно: сначала простые тесты и ручное закрепление базовых конструкций, затем рефакторинг, выделение повторяющейся логики и построение более полноценной архитектуры автотестов.

README подготовлен с помощью ChatGPT и отредактирован вручную.

Код тестов пишется самостоятельно в рамках обучения. ChatGPT используется как ментор для объяснения теории, ревью решений и разбора ошибок.