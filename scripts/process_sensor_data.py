import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from sqlalchemy import select
from sqlalchemy.orm import Session
from models.models import RawData, AvgData
from scripts.db.vanilla_db import get_engine_and_session
from functools import reduce

ONE_HOUR = 3600


def round_down_to_hour(timestamp):
    return timestamp - (timestamp % ONE_HOUR)


def not_none(row):
    return row.value is not None


def add_totals(running_total, row):
    addition = row.value

    return running_total + addition


def average_raw_data_loop():
    # Create standalone version of the engine, so it's not reliant on Flask running.
    engine, SessionLocal = get_engine_and_session()

    start_time = datetime.datetime.now().timestamp()
    oldest_query = select(RawData.timestamp).order_by(RawData.timestamp.asc()).limit(1)

    with SessionLocal() as session:
        oldest_timestamp = session.execute(oldest_query).scalar_one_or_none()

    if oldest_timestamp:
        oldest_hour_floor = round_down_to_hour(oldest_timestamp)
    else:
        oldest_hour_floor = None
        print("No Data in DB yet, entering waiting mode...")

    if oldest_hour_floor:
        while oldest_hour_floor < start_time:
            average_raw_data(oldest_hour_floor, engine)
            oldest_hour_floor += ONE_HOUR


def average_raw_data(timestamp_to_process, engine):
    one_hour_ago = timestamp_to_process - ONE_HOUR

    print(f"Timestamp to process is: {timestamp_to_process}")
    print(f"An hour ago is: {one_hour_ago}")

    query = select(RawData).filter(
        (RawData.timestamp >= one_hour_ago)
        & (RawData.timestamp <= timestamp_to_process)
    )

    with Session(engine) as session:
        rows = session.execute(query).scalars().all()

    pruned_avg_data = list(filter(not_none, rows))

    reading_count = len(pruned_avg_data)

    total_reading_value = reduce(add_totals, pruned_avg_data, 0)

    if reading_count > 0:
        average_reading = round(total_reading_value / reading_count)
    else:
        average_reading = None

    write_to_db(one_hour_ago, average_reading, engine)


def write_to_db(one_hour_ago, average_reading, engine):
    with Session(engine) as session:
        # Check if one hour ago already exists.
        existing_record = (
            session.query(AvgData)
            .filter(AvgData.timestamp == one_hour_ago)
            .one_or_none()
        )

        # If it does, update the value.
        if existing_record:
            existing_record.value = average_reading
            print(
                f"Updated DB -- TIMESTAMP: {one_hour_ago}, READING: {average_reading}"
            )
        else:
            # If not, insert it.
            new_record = AvgData(timestamp=one_hour_ago, value=average_reading)
            session.add(new_record)
            print(
                f"Inserted DB -- TIMESTAMP: {one_hour_ago}, READING: {average_reading}"
            )

        session.commit()


def main():
    average_raw_data_loop()
    print("Entering wait mode...")
    scheduler = BlockingScheduler()
    scheduler.add_job(average_raw_data_loop, "interval", hours=1)
    scheduler.start()


if __name__ == "__main__":
    main()
