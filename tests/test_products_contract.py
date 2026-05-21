import requests
from helpers.assert_product_contract import assert_product_contract
from helpers.assert_required_list_field import assert_required_list_field

def test_products_contract_all_items():
    base_url = "https://api.practicesoftwaretesting.com"
    response = requests.get(base_url + "/products", timeout=10)

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)
    assert_required_list_field(data, "data", "root")
    assert len(data["data"]) > 0

    items = data["data"]

    for index, item in enumerate(items):
        assert_product_contract(item, index)
