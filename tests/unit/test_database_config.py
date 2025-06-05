def test_abc(client, db_session):
    db_location = db_session.get_bind().url
    print(db_location)

    assert "memory" in str(db_location)
