from helpers.assert_required_string_field import assert_required_string_field


def assert_brand_contract(index, item):
    assert_required_string_field(item, "id", index)
    assert_required_string_field(item, "name", index)
    assert_required_string_field(item, "slug", index)
