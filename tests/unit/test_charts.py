from models.models import AvgData


def test_charts_route_returns_ok(client):
    response = client.get("/charts")
    assert response.status_code == 200


def test_charts_empty_chart(client):
    response = client.get("/charts")
    assert b'canvas id="chart"' in response.data


def test_charts_value(client, db_session, mocker):
    fixed_time = 1750000000
    mocker.patch("time.time", return_value=fixed_time)

    row = AvgData(timestamp=1749500000, value=66)
    db_session.add(row)
    db_session.commit()

    response = client.get("/charts")
    html = response.data.decode("utf-8")

    # Asserting based off MILLISECONDS!
    # The value gets converted for charts.js
    assert "1749500000000" in html
