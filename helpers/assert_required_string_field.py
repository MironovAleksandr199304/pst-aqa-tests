def assert_required_string_field(item, field, index):
    assert field in item, (
        f"Поле {field} у объекта с индексом {index} ожидалось в ответе, но его нет."
    )

    assert isinstance(item[field], str), (
        f"Поле {field} у объекта с индексом {index} ожидалось типа str,"
        f"но вернулось {type(item[field])}"
    )

    assert item[field] != "", (
        f"Ожидалось, что поле {field} у объекта с индексом {index} не будет пустым,"
        f"но оно пустое: {item[field]}"
    )
