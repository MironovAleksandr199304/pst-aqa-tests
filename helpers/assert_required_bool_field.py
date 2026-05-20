def assert_required_bool_field(item, field, index):
    assert field in item, (
        f"Ожидалось что в ответе будет поле {field}.Но его нет. Вообще."
    )
    assert isinstance(item[field], bool), (
        f"Ожидалось что поле {field} у объекта с индексом {index} будет иметь тип bool. Но он не бул. Вот так."
    )
