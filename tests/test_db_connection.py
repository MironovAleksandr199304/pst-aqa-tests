def test_db_connection(db_client):
    result = db_client.fetch_one("SELECT 1")
    assert result is not None
    assert result[0] == 1
