import requests

from helpers.assert_brand_contract import assert_brand_contract


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
        assert_brand_contract(index, item)
