import serial
import time
import sqlite3
import datetime
import random
from dateutil import parser

connection = sqlite3.connect("plant_info.db")
cursor = connection.cursor()

#Set this to 1 if you need to recreate the db.
create_moist_db = 0

if create_moist_db == 1:
    cursor.execute("create table moist (date_time text, wetness integer)")

"""
arduino = serial.Serial(port='/dev/ttyACM0',   baudrate=115200, timeout=.1)

readings = []

def write_read():
    arduino.write(bytes(1))
    time.sleep(0.1)
    data = arduino.readline()
    return data


while True:
    time.sleep(10)

    value = write_read()
    print(type(value))
    new_value = int(value.decode('utf-8'))
    readings.append(new_value)
    
    print(readings)
"""  

#Function to check the water level in the tomatoes.
def moistCheck():
    #Return a random value for now.
    return(random.randint(0,100))

"""
value = "2011-11-04"

#Make a time into ISO 8601 Format
print(parser.isoparse(value))

#Get current time?
current_time = (time.ctime())
   
now = datetime.datetime.now()
today = datetime.date.today()
now = datetime.datetime.now()
print(now)

#now = now.strftime("%Y-%m-%d %H:%M:%S")
now_time = now.strftime("%H:%M:%S")
print(now_time)
"""

def main():
    
    #Gets the time since epoch
    epoch_time = int(time.time())
    
    #Modulus the time by the seconds in 1 hour to check if the time is exactly an hour
    mod_epoch = (epoch_time%3600)
    print(f"MOD Epoch = {mod_epoch}") #DEBUG PRINT that value


    #if mod_epoch == 0: DELETE THE COMMENT WHEN YOU NEED HOURLY RUNS
    current_moist = moistCheck()
    
    #Put the values into the DB
    #print(current_moist)
    cursor.execute("INSERT INTO moist (date_time, wetness) VALUES (?, ?)", (epoch_time, current_moist))

    #print database rows
    for row in cursor.execute("select * from moist"):
        print(row)
   

#Run Program
main()

connection.close()