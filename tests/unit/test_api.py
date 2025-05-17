def test_chart_api_readings(client, mocker):
    rows = [[12345, 10], [12346, 20], [12347, 30]]

    mock_db_fetch = mocker.patch("db.fetch_between", return_value=rows)
    response = client.get("/api/readings")

    json_data = response.get_json()
    assert json_data[0]["x"] == 12345000
    assert json_data[0]["y"] == 10


# Test that the json modifys the timestamp by 1000

# Test that it passes the value directly

# That that it passes the same number of points through

# Test when there's no data. (I think this will fail)

# Test when data is None/Null

# Test when the timeframe parameter maps to the correct windows (1d, 1w, 1m) (probably need to mock time)


# NOTE ALSO FIX THE BROKEN EXTRA TABLE IN DATABSE.
