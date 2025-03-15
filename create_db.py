import sqlite3

recreate_db_flag = 1

if recreate_db_flag == 1:
    connection = sqlite3.connect("plant_info.db")
    cursor = connection.cursor()
    cursor.execute("create table minute_reading (date_time text, moisture_reading integer)")
    connection.close()
