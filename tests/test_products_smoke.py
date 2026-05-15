import requests

def test_smoke_product():
    response = requests.get("https://api.practicesoftwaretesting.com/products", timeout=5)
    assert response.status_code == 200

def test_smoke_brands():
    response = requests.get("https://api.practicesoftwaretesting.com/brands", timeout=10)
    print(response.headers)
    assert response.status_code == 200