def test_db_insert_select(db_client):
    db_client.execute_query("CREATE TABLE IF NOT EXISTS test_users "
                            "(user_id INT PRIMARY KEY,"
                            "user_name VARCHAR)")
    db_client.execute_query("TRUNCATE TABLE test_users")

    query = ("INSERT INTO test_users (user_id, user_name) VALUES"
             "(%s, %s)")
    params = (1, "BESTAQASASHA")

    db_client.execute_query(query, params)

    query_select = "SELECT user_id, user_name FROM test_users WHERE user_id = %s"
    params = (1,)
    result = db_client.fetch_one(query_select, params)
    assert result is not None
    assert result[0] == 1
    assert result[1] == "BESTAQASASHA"