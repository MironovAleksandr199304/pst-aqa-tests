from helpers.assert_brand_contract import assert_brand_contract


def test_api_brand_saved_to_db(db_client, brands_client):
    response = brands_client.get_brands()
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list), (
        f"FAIL: ответ имеет другой тип, отличный от list"
    )

    assert len(data) > 0, (
        f"FAIL: ответ пустой"
    )

    first_item = data[0]
    index = 0
    assert_brand_contract(index, first_item)

    query_create = ("CREATE TABLE IF NOT EXISTS test_brands"
                    "(id VARCHAR PRIMARY KEY,"
                    "name VARCHAR NOT NULL,"
                    "slug VARCHAR NOT NULL)")
    db_client.execute_query(query_create)

    query_truncate = ("TRUNCATE TABLE test_brands")
    db_client.execute_query(query_truncate)

    query_insert = ("INSERT INTO test_brands (id, name, slug) VALUES "
                    "( %s, "
                    " %s, "
                    " %s )")
    params = (first_item["id"], first_item["name"], first_item["slug"])
    db_client.execute_query(query_insert, params)

    query_select = ("SELECT id, name, slug FROM test_brands"
                    " WHERE id = %s"
                    )
    params = (first_item["id"],)
    result = db_client.fetch_one(query_select, params)

    assert result is not None
    assert result[0] == first_item["id"]
    assert result[1] == first_item["name"]
    assert result[2] == first_item["slug"]
