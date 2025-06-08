import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from app.db.models import AvgData, RawData

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

ONE_HOUR = 3600


def round_down_to_hour(timestamp):
    return timestamp - (timestamp % ONE_HOUR)


# Create standalone version of the engine, so it's not reliant on Flask running.
engine = create_engine("sqlite:///instance/plant_info.db", future=True)


def average_raw_data_loop():
    start_time = datetime.datetime.now().timestamp()
    oldest_query = select(RawData.timestamp).order_by(RawData.timestamp.asc()).limit(1)

    with Session(engine) as session:
        oldest_timestamp = session.execute(oldest_query).scalar_one_or_none()

    if oldest_timestamp:
        oldest_hour_floor = round_down_to_hour(oldest_timestamp)
    else:
        oldest_hour_floor = None
        print("No Data in DB yet, entering waiting mode...")

    if oldest_hour_floor:
        while oldest_hour_floor < start_time:
            average_raw_data(oldest_hour_floor)
            oldest_hour_floor += ONE_HOUR


def average_raw_data(timestamp_to_process):
    one_hour_ago = timestamp_to_process - ONE_HOUR

    print(f"Timestamp to process is: {timestamp_to_process}")
    print(f"An hour ago is: {one_hour_ago}")

    query = select(RawData).filter(
        (RawData.timestamp >= one_hour_ago)
        & (RawData.timestamp <= timestamp_to_process)
    )

    with Session(engine) as session:
        rows = session.execute(query).scalars().all()

    reading_count = 0
    total_reading_value = 0

    for row in rows:
        reading_count += 1
        total_reading_value += row.value

    if reading_count > 0:
        average_reading = round(total_reading_value / reading_count)
    else:
        average_reading = None

    write_to_db(one_hour_ago, average_reading)


def write_to_db(one_hour_ago, average_reading):
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
