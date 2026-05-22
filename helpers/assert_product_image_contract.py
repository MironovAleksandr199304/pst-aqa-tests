from helpers.assert_required_string_field import assert_required_string_field


def assert_product_image_contract(item, index):
    assert isinstance(item, dict)
    assert_required_string_field(item, "id", index)
    assert_required_string_field(item, "by_name", index)
    assert_required_string_field(item, "by_url", index)
    assert_required_string_field(item, "source_name", index)
    assert_required_string_field(item, "source_url", index)
    assert_required_string_field(item, "file_name", index)
    assert_required_string_field(item, "title", index)