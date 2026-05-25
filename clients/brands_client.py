import requests

class BrandsClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_brands(self):
        response = requests.get(self.base_url + "/brands", timeout=10)
        return response