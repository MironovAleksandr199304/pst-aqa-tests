import requests

def test_brands_contract():
    base_url = "https://api.practicesoftwaretesting.com"
    response = requests.get(base_url+"/brands", timeout=10)

    assert response.status_code == 200,(
        f"Ожидается статус 200, но возвращает {response.status_code}."
        f"Body: {response.text[:500]}"
    )
    data = response.json()
    assert isinstance(data,list),(
        f"Ответ должен быть с типом list, но возвращает {type(data)}"
    )
    assert len(data)>0, (
        f"Endpoint /brands GET вернул пустой списоак: {data}"
    )

    first_item = data[0]

    assert isinstance(first_item,dict), (
        f"Первый объект в ответе /brands GET должен быть dict, но возвращает {type(first_item)}"
    )

    assert "id" in first_item, (
        f"Endpoint /brands не содержит поле id"
    )
    assert isinstance(first_item["id"],str), (
        f"Endpoint /brands поле id имеет некорректный тип: {type(first_item['id'])}"
    )
    assert first_item["id"] != "", (
        f"Endpoint /brands GET возвращает пустое значение в поле id: {first_item['id']}"
    )
    assert "name" in first_item,(
        f"Endpoint /brands GET не содержит поле name"
    )
    assert isinstance(first_item["name"],str), (
        f"Endpoint /brands GET поле name имеет некорректный тип: {type(first_item['name'])}"
    )
    assert first_item["name"] != "", (
        f"Endpoint /brands GET возвращает пустое значение в поле name: {first_item['name']}"
    )
    assert "slug" in first_item, (
        f"Endpoint /brands GET не содержит поле slug"
    )
    assert isinstance(first_item["slug"],str),(
        f"Endpoint /brands GET поле slug имеет некорректный тип: {type(first_item['slug'])}"
    )
    assert first_item["slug"] != "",(
        f"Endpoint /brands GET возвращает пустое значение в поле slug: {first_item['slug']}"
    )