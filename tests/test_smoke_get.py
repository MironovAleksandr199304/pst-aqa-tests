import pytest
import requests

@pytest.mark.parametrize("endpoint,expected_status", [
    ("/products", 200),
    ("/brands", 200),
    ("/categories", 200),
    ("/categories/tree", 200),
    ("/brands/search", 200),
    ("/messages", 401),
    ("/favorites", 401)
])
def test_get_smoke(endpoint,expected_status):
    base_url = "https://api.practicesoftwaretesting.com"
    headers = {"Accept" : "application/json"}
    response = requests.get(base_url + endpoint, headers=headers, timeout=10)
    assert response.status_code == expected_status,(
        f"{endpoint} returned {response.status_code}, "
        f"expected {expected_status}. Body: {response.text[:500]}"
    )