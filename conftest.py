import pytest

from clients.products_client import ProductsClient
from clients.brands_client import BrandsClient
from db.db_client import DbClient
from db.db_config import get_db_config


@pytest.fixture
def base_url():
    return "https://api.practicesoftwaretesting.com"


@pytest.fixture
def product_client(base_url):
    return ProductsClient(base_url)


@pytest.fixture
def brands_client(base_url):
    return BrandsClient(base_url)


@pytest.fixture
def db_config():
    return get_db_config()


@pytest.fixture
def db_client(db_config):
    return DbClient(db_config)