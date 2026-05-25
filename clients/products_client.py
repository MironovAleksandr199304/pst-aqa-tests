import requests


class ProductsClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_products(self):
        response = requests.get(self.base_url + "/products", timeout=10)
        return response
