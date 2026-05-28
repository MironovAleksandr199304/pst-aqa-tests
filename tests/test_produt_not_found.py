def test_product_not_found(product_client):
    product_id = 999
    response = product_client.get_product_by_id(product_id)
    assert response.status_code == 404

    content_type = response.headers.get("Content-Type", "").lower()

    assert "application/json" in content_type, (
        "ожидали JSON, но Content-Type не содержит application/json"
    )
    data = response.json()
    assert data["message"] == "Requested item not found"