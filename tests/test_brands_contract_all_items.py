import requests


def test_brands_contract_all_items():
    base_url = "https://api.practicesoftwaretesting.com"
    response = requests.get(base_url + "/brands", timeout=10)
    assert response.status_code == 200, (
        f"GET /brands вернул статус {response.status_code}, ожидалось 200."
        f"Body: {response.text[:500]}"
    )

    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0, (
        f"Длина списка в ответе должна была быть больше 0, вернуло {len(data)}"
        f"Body: {data}"
    )

    for index, item in enumerate(data):
        assert "id" in item, (
            f"В ответе должно быть поле id у чувака с индексом {index}, но его, увы, нет."
        )
        assert isinstance(item["id"], str), (
            f"Поле id у чувака с индексом {index} должно иметь тип string. Но почему-то оно другое."
        )
        assert item["id"] != "", (
            f"Поле id у чувака с индексом {index} не должно быть пустым. Никак. Это же id. Но оно пустое..."
        )
        assert "name" in item, (
            f"В ответе должно быть поле name у чувака с индексом {index}, но его, увы, нет."
        )
        assert isinstance(item["name"], str), (
            f"Поле name у чувака с индексом {index} должно иметь тип string. Но кто-то решил иначе."
        )
        assert item["name"] != "", (
            f"Поле name у чувака с индексом {index} не должно быть пустым. Не дело это. Но оно пустое..."
        )
        assert "slug" in item, (
            f"В ответе у чувака с индексом {index} должно быть поле slug. Но его почему-то нет, и это не я."
        )
        assert isinstance(item["slug"], str), (
            f"Поле slug у чувака с индексом {index} должно быть типа string. Но оно типа не string. Странно."
        )
        assert item["slug"] != "", (
            f"Поле slug у чувака с индексом {index} по-хорошему должно быть заполнено. Но почему-то оно пустое. Не дело..."
        )
