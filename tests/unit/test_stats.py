def test_check_heading_rendered(client, mocker):
    mocker.patch("db.fetch", side_effect=[50, 100, 75])
    response = client.get("/stats")
    assert b"Minimum Moisture Recorded" in response.data


def test_check_min_moisture(client, mocker):
    mocker.patch("db.fetch", side_effect=[50, 100, 75])
    response = client.get("/stats")
    assert b'<td id="min-moisture">50</td>' in response.data
    assert b'<td id="max-moisture">100</td>' in response.data
    assert b'<td id="avg-moisture">75</td>' in response.data
