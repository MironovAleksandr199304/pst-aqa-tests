import requests


class ProductsClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_products(self):
        response = requests.get(self.base_url + "/products", timeout=10)
        return response

    def get_product_by_id(self, product_id):
        response = requests.get(f"{self.base_url}/products/{product_id}", timeout=10)
        return response
