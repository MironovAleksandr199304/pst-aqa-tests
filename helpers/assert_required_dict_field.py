def assert_required_dict_field(item, field, index):
    assert field in item, (
        f"Ожидалось, что в объекте с индексом {index} будет поле {field}. Но не тут то было."
    )

    assert isinstance(item[field], dict), (
        f"Ожидалось что {field} у индекса {index} будет словариком. Но он не словарик. Он кто-то другой."
    )
