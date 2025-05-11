import sqlite3

recreate_raw_db_flag = 0
recreate_avg_db_flag = 0
recreate_data_checkpoint_flag = 1

if recreate_raw_db_flag == 1:
    connection = sqlite3.connect("plant_info.db")
    cursor = connection.cursor()
    cursor.execute(
        "create table minute_reading (date_time integer, moisture_reading integer)"
    )
    connection.close()

if recreate_avg_db_flag == 1:
    connection = sqlite3.connect("plant_info.db")
    cursor = connection.cursor()
    cursor.execute(
        "create table avg_data (date_time integer UNIQUE, readable_time text UNIQUE, moisture_reading integer)"
    )
    connection.close()

if recreate_data_checkpoint_flag == 1:
    connection = sqlite3.connect("plant_info.db")
    cursor = connection.cursor()
    cursor.execute("create table data_checkpoint (key text , last_finalised integer)")
    connection.close()
