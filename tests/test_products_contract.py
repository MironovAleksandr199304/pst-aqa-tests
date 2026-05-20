import requests

from helpers.assert_required_number_field import assert_required_number_field
from helpers.assert_required_string_field import assert_required_string_field

def test_products_contract_all_items():
    base_url = "https://api.practicesoftwaretesting.com"
    response = requests.get(base_url + "/products", timeout=10)

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)
    assert "data" in data
    assert isinstance(data["data"], list)
    assert len(data["data"]) > 0

    items = data["data"]

    for index, item in enumerate(items):
        assert_required_string_field(item,"id",index)
        assert_required_string_field(item,"name",index)
        assert_required_string_field(item,"description",index)
        assert_required_number_field(item,"price",index)
