from models.models import RawData
from app.index.home import translate_moisture


def describe_translate_moisture():
    def test_translate_moisture_25():
        returned_result = translate_moisture(25, 200)
        assert "Moisture levels critical." in returned_result
        assert "12%" in returned_result

    def test_translate_moisture_75():
        returned_result = translate_moisture(75, 213)
        assert "Moisture levels balanced." in returned_result
        assert "35%" in returned_result

    def test_translate_moisture_125():
        returned_result = translate_moisture(125, 226)
        assert "Moisture within acceptable parameters." in returned_result
        assert "55%" in returned_result

    def test_translate_moisture_175():
        returned_result = translate_moisture(175, 378)
        assert "Moisture decreasing." in returned_result
        assert "46%" in returned_result

    def test_translate_moisture_225():
        returned_result = translate_moisture(225, 9999)
        assert "Warning: Dry conditions detected." in returned_result
        assert "2%" in returned_result

    def test_translate_moisture_275():
        returned_result = translate_moisture(275, 13)
        assert "Alert: Severe dehydration likely." in returned_result
        assert "2115%" in returned_result

    def test_translate_moisture_325():
        returned_result = translate_moisture(325, 325)
        assert "CRITICAL STATUS!" in returned_result
        assert "0%" in returned_result

    def test_translate_moisture_out_of_bounds():
        returned_result = translate_moisture(9999, 10000)
        assert "Reading outside expected parameters" in returned_result
        assert "%" not in returned_result

    def test_translate_moisture_string():
        returned_result = translate_moisture("ABCD", "XYZ")
        assert "Non numberic values provided. Consult administrator" in returned_result
        assert "%" not in returned_result


def test_show_homepage(client, db_session):
    row = RawData(timestamp=5000, value=66)
    db_session.add(row)

    row = RawData(timestamp=10000, value=33)
    db_session.add(row)

    db_session.commit()

    response = client.get("/")

    assert response.status_code == 200
    assert b"Moisture levels critical" in response.data
    assert b"33" in response.data
