def assert_required_number_field(item, field, index):
    assert field in item, (
        f"В ответе у объекта с индексом {index} ожидалось поле {field}. Но его нет."
    )
    assert type(item[field]) != bool, (
        f"Ожидалось, что поле {field} у объекта с индексом {index} имеет не булевой тип. Но он булевой, увы."
    )
    assert isinstance(item[field], int) or isinstance(item[field], float), (
        f"Ожидалось, что поле {field} у объекта с индексом {index} имеет тип int или float. Но это не так."
    )



