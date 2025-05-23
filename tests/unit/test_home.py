from app.index.home import translate_moisture
from app import create_app
from unittest.mock import patch, MagicMock


def describe_translate_moisture():
    def test_translate_moisture_25(mocker):
        number = mocker.patch("db.fetch", return_value=200)
        returned_result = translate_moisture(25)
        assert "Moisture levels critical." in returned_result
        assert "12%" in returned_result

    def test_translate_moisture_75(mocker):
        number = mocker.patch("db.fetch", return_value=213)
        returned_result = translate_moisture(75)
        assert "Moisture levels balanced." in returned_result
        assert "35%" in returned_result

    def test_translate_moisture_125(mocker):
        number = mocker.patch("db.fetch", return_value=226)
        returned_result = translate_moisture(125)
        assert "Moisture within acceptable parameters." in returned_result
        assert "55%" in returned_result

    def test_translate_moisture_175(mocker):
        number = mocker.patch("db.fetch", return_value=378)
        returned_result = translate_moisture(175)
        assert "Moisture decreasing." in returned_result
        assert "46%" in returned_result

    def test_translate_moisture_225(mocker):
        number = mocker.patch("db.fetch", return_value=9999)
        returned_result = translate_moisture(225)
        assert "Warning: Dry conditions detected." in returned_result
        assert "2%" in returned_result

    def test_translate_moisture_275(mocker):
        number = mocker.patch("db.fetch", return_value=13)
        returned_result = translate_moisture(275)
        assert "Alert: Severe dehydration likely." in returned_result
        assert "2115%" in returned_result

    def test_translate_moisture_325(mocker):
        number = mocker.patch("db.fetch", return_value=325)
        returned_result = translate_moisture(325)
        assert "CRITICAL STATUS!" in returned_result
        assert "100%" in returned_result

    def test_translate_moisture_out_of_bounds(mocker):
        number = mocker.patch("db.fetch", return_value=3)
        returned_result = translate_moisture(9999)
        assert "Reading outside expected parameters" in returned_result
        assert "%" not in returned_result

    def test_translate_moisture_string(mocker):
        number = mocker.patch("db.fetch", return_value=200)
        returned_result = translate_moisture("ABCD")
        assert "Non numberic values provided. Consult administrator" in returned_result
        assert "%" not in returned_result


def test_show_homepage(monkeypatch):
    app = create_app()  # Or however you instantiate your Flask app
    app.testing = True

    # Mock the database connection and cursor
    mock_connection = MagicMock()
    mock_cursor = MagicMock()

    # Returns (1,500) whenever fetchone is called on the cursor.
    mock_cursor.fetchone.return_value = (None, 245)
    # Returns the mock_cursor obeject whenever .cursor is used on connection.
    mock_connection.cursor.return_value = mock_cursor

    # Make a new function that simulates just the rendering of one instance of getting the
    # error message into the HTML (I've tested mock translate in full above)
    def mock_translate(reading):
        return "Moisture decreasing. <br/> Recommend hydration soon to avoid cellular stress."

    # Patch the original translate moisture to be replaced with the mocked function.
    monkeypatch.setattr("app.index.home.translate_moisture", mock_translate)

    # Replaces the real DB with the fake one for testing
    with patch("db.get_connection", return_value=mock_connection):
        # Uses a fake web browser
        with app.test_client() as client:
            # Fake visits the homepage.
            response = client.get("/")

            # Do tests here.
            assert response.status_code == 200
            assert b"Moisture decreasing" in response.data
