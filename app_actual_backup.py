from flask import Flask, render_template
import sqlite3
import random
import time

app = Flask(__name__)

box_colours_dict = {
    "wet-0" : "#F9E79F", 
    "wet-20" : "#F4D03F",
    "wet-40" : "#A3D77E",
    "wet-60": "#5D8B93",
    "wet-80": "#2471A3",
    "wet-100" : "#1D4E89"
}



#Set this to 1 if you need to recreate the table.
create_moist_db = 0

if create_moist_db == 1:
    connection = sqlite3.connect("plant_info.db")
    cursor = connection.cursor()
    cursor.execute("create table moist (date_time text, wetness integer, box_colour text)")
    cursor.execute("create table hourly (date_time text, wetness integer, box_colour text)")

#Function to check the water level in the tomatoes.
def moistCheck(last_generated):
   
    #Generate a random adjustment to the current wetness level
    adjustment = random.randint(4,15)
    #Randomise either an addition or a subtraction
    add = random.randint(0,1)

    #Ensure the value cannot exceed 100
    if add == 1 and last_generated + adjustment > 100:
        return 100
    
    #Ensure the value cannot be a minus
    if add == 0 and last_generated - adjustment < 0:
        return 0

    #Adjust the previous value, and then return
    if add == 1:
        last_generated += adjustment
    else:
        last_generated -= adjustment

    return last_generated
    
def box_colour_assign(last_generated):  
    if last_generated < 10:
        return box_colours_dict["wet-0"]
    elif last_generated < 20:
        return box_colours_dict["wet-20"]
    elif last_generated < 40:
        return box_colours_dict["wet-40"]
    elif last_generated < 60:
        return box_colours_dict["wet-60"]
    elif last_generated < 80:
        return box_colours_dict["wet-80"]
    elif last_generated <= 100:
        return box_colours_dict["wet-100"]
    

# Function to get the latest data from the database
def check_moisture():

    # Connect to the database
    connection = sqlite3.connect("plant_info.db")
    cursor = connection.cursor()

    #Gets the time since epoch
    epoch_time = int(time.time())
    
    #Modulus the time by the seconds in 1 hour to check if the time is exactly an hour
    mod_epoch = (epoch_time%3600)
    print(f"MOD Epoch = {mod_epoch}") #DEBUG PRINT that value

    #if mod_epoch == 0: DELETE THE COMMENT WHEN YOU NEED HOURLY RUNS
    #current_moist = moistCheck()
    
    #Define the starting number for the randomly generated readings.
    last_generated = 50
    
    for i in range (28):
        last_generated = moistCheck(last_generated)
        box_colour = box_colour_assign(last_generated)

        cursor.execute("INSERT INTO moist (date_time, wetness, box_colour) VALUES (?, ?, ?)", (epoch_time, last_generated, box_colour))

    connection.commit()
    connection.close()

"""
Array [
    [date_time, wetness, box_colour],
    [date_time, wetness, box_colour],
]

Array2 [
    {"percent" : 12, "colour" : "green",},
    {"percent" : 12, "colour" : "blue",},
    
]

moisture_day = {
    "percent" : 12,
    "colour" : "Green"
}
"""


def to_model(row):

    model = {
        "date_time" : row[0],
        "percent" : row[1],
        "box_colour" : row[2],
    }
    #print(model)
    return model

@app.route('/')
def index():
    check_moisture()

    #Reconnect to the DB
    connection = sqlite3.connect("plant_info.db")
    cursor = connection.cursor()

    #Fetch the last 30 entries of moisture data from the database and assign them to a variable
    cursor.execute("SELECT * FROM moist ORDER BY date_time DESC LIMIT 28")
    rows = cursor.fetchall()  

    #Get all the moisture levels
    #cursor.execute("SELECT * FROM moist ORDER BY date_time DESC LIMIT 1")

    # Close the connection
    connection.close()

    fake = [{"percent" : 23, "box_colour" : "green"}]

    # Give data to the html
    #return render_template('index.html', monthly_moisture=monthly_moisture)
    #return render_template('index.html', monthly_moisture=map(to_model,rows))
    #print(list(map(to_model,rows)))
    return render_template('index.html', monthly_moisture=list(map(to_model,rows)))

if __name__ == "__main__":
    app.run(debug=True)

