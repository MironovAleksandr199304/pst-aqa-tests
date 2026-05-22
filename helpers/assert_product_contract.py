from helpers.assert_required_string_field import assert_required_string_field
from helpers.assert_required_number_field import assert_required_number_field
from helpers.assert_required_bool_field import assert_required_bool_field
from helpers.assert_required_dict_field import assert_required_dict_field
from helpers.assert_product_brand_contract import assert_product_brand_contract
from helpers.assert_product_category_contract import assert_product_category_contract
from helpers.assert_product_image_contract import assert_product_image_contract


def assert_product_contract(item, index):
    assert isinstance(item, dict)
    assert_required_string_field(item, "id", index)
    assert_required_string_field(item, "name", index)
    assert_required_string_field(item, "description", index)
    assert_required_number_field(item, "price", index)
    assert_required_bool_field(item, "is_location_offer", index)
    assert_required_bool_field(item, "is_rental", index)
    assert_required_string_field(item, "co2_rating", index)
    assert_required_bool_field(item, "in_stock", index)
    assert_required_bool_field(item, "is_eco_friendly", index)
    assert_required_dict_field(item, "product_image", index)
    assert_product_image_contract(item["product_image"], index)
    assert_required_dict_field(item, "category", index)
    assert_product_category_contract(item["category"], index)
    assert_required_dict_field(item, "brand", index)
    assert_product_brand_contract(item["brand"], index)
