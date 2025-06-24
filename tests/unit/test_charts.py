def test_charts_route_returns_ok(client):
    response = client.get("/charts")
    assert response.status_code == 200
