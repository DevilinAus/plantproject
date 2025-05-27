from app.index.home import translate_moisture


def describe_translate_moisture():
    def test_translate_moisture_25(mocker):
        mocker.patch("db.fetch", return_value=200)
        returned_result = translate_moisture(25)
        assert "Moisture levels critical." in returned_result

    def test_translate_moisture_75(mocker):
        mocker.patch("db.fetch", return_value=200)
        returned_result = translate_moisture(75)
        assert "Moisture levels balanced." in returned_result

    def test_translate_moisture_125(mocker):
        mocker.patch("db.fetch", return_value=200)
        returned_result = translate_moisture(125)
        assert "Moisture within acceptable parameters." in returned_result

    def test_translate_moisture_175(mocker):
        mocker.patch("db.fetch", return_value=200)
        returned_result = translate_moisture(175)
        assert "Moisture decreasing." in returned_result

    def test_translate_moisture_225(mocker):
        mocker.patch("db.fetch", return_value=200)
        returned_result = translate_moisture(225)
        assert "Warning: Dry conditions detected." in returned_result

    def test_translate_moisture_275(mocker):
        mocker.patch("db.fetch", return_value=200)
        returned_result = translate_moisture(275)
        assert "Alert: Severe dehydration likely." in returned_result

    def test_translate_moisture_325(mocker):
        mocker.patch("db.fetch", return_value=200)
        returned_result = translate_moisture(325)
        assert "CRITICAL STATUS!" in returned_result

    def test_translate_moisture_out_of_bounds(mocker):
        mocker.patch("db.fetch", return_value=200)
        returned_result = translate_moisture(9999)
        assert "Reading outside expected parameters" in returned_result

    def test_translate_moisture_string(mocker):
        mocker.patch("db.fetch", return_value=200)
        returned_result = translate_moisture("ABCD")
        assert "Non numberic values provided. Consult administrator" in returned_result
