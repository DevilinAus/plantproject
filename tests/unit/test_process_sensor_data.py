from models.models import AvgData, RawData
from scripts.process_sensor_data import average_raw_data


from sqlalchemy import select

from scripts.process_sensor_data import round_down_to_hour


def describe_average_raw_data():
    def test_round_down_to_hour():
        returned_ts = round_down_to_hour(1754913805)
        assert returned_ts == 1754913600

    def test_average_multiple_values(raw_session):
        timestamp_to_process = 1686495605 + 3600

        seed_data = [
            RawData(timestamp=1686495605, value=90),
            RawData(timestamp=1686495623, value=100),
            RawData(timestamp=1686495734, value=110),
        ]

        raw_session.add_all(seed_data)
        raw_session.commit()

        average_raw_data(timestamp_to_process, raw_session.get_bind())

        query = select(AvgData)

        average = raw_session.scalars(query).one()

        assert average.timestamp == 1686495605
        assert average.value == 100

    def test_averages_single_value(raw_session):
        timestamp_to_process = 1686495605 + 3600

        seed_data = [RawData(timestamp=1686495605, value=90)]

        raw_session.bulk_save_objects(seed_data)
        raw_session.commit()

        average_raw_data(timestamp_to_process, raw_session.get_bind())

        query = select(AvgData)

        average = raw_session.scalars(query).one()

        assert average.timestamp == 1686495605
        assert average.value == 90
