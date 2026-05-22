from helpers.assert_required_string_field import assert_required_string_field

def assert_product_brand_contract(item, index):
    assert isinstance(item, dict)
    assert_required_string_field(item, "id", index)
    assert_required_string_field(item, "name", index)
