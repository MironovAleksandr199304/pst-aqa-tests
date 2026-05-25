def test_db_fetch_all(db_client):
    result = db_client.fetch_all("SELECT 1 "
                                 " UNION ALL "
                                 " SELECT 2")
    assert result is not None
    assert len(result) == 2
    assert result[0][0] == 1
    assert result[1][0] == 2
