def assert_required_list_field(item,field,index):
    assert field in item, (
        f"В объекте с индексом {index} ожидалось поле {field}. Но его нет."
    )

    assert isinstance(item[field],list), (
        f"Ожидалось, что {field} имеет тип list, но"
        f"у него {type(item[field])}"
    )

