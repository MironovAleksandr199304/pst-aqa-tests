def test_api_product_saved_to_db(product_client, db_client):
    response = product_client.get_products()
    assert response.status_code == 200
    data = response.json()
    first_item = data["data"][0]

    query = ("CREATE TABLE IF NOT EXISTS test_products "
             "(id VARCHAR PRIMARY KEY,"
             "name VARCHAR,"
             "price FLOAT)")
    db_client.execute_query(query)
    query_truncate = ("TRUNCATE TABLE test_products")
    db_client.execute_query(query_truncate)
    query_insert = ("INSERT INTO test_products (id, name, price) VALUES"
                    " (%s, %s, %s)")
    params = (first_item["id"], first_item["name"], first_item["price"])
    db_client.execute_query(query_insert, params)

    query_select = ("SELECT id, name, price FROM test_products"
                    " WHERE id = %s ")
    params = (first_item["id"],)
    result = db_client.fetch_one(query_select, params)
    assert result is not None
    assert result[0] == first_item["id"]
    assert result[1] == first_item["name"]
    assert result[2] == first_item["price"]
