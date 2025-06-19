def test_using_memory_db_flask(client, db_session):
    db_location = db_session.get_bind().url

    assert "memory" in str(db_location)


def test_using_memory_db_vanilla(raw_session):
    db_location = raw_session.get_bind().url

    assert "memory" in str(db_location)
