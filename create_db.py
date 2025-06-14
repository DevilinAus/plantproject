from db import get_connection

recreate_raw_db_flag = 0
recreate_avg_db_flag = 0
recreate_data_checkpoint_flag = 0
recreate_current_weather_flag = 1

if recreate_raw_db_flag == 1:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "create table raw_data (date_time integer, moisture_reading integer)"
    )
    connection.close()

if recreate_avg_db_flag == 1:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "create table avg_data (date_time integer UNIQUE, moisture_reading integer)"
    )
    connection.close()

# CURRENTLY UNUSED.
# if recreate_data_checkpoint_flag == 1:
#     connection = get_connection()
#     cursor = connection.cursor()
#     cursor.execute("create table data_checkpoint (key text , last_finalised integer)")
#     connection.close()

if recreate_current_weather_flag == 1:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("create table current_weather (key text UNIQUE, value TEXT)")
    connection.close()
