from flask import Flask, render_template
from flask import Blueprint
from datetime import datetime
import sqlite3
import random
import time

daily_chart_bp = Blueprint('daily_chart', __name__, template_folder='templates')

@daily_chart_bp.route('/daily_chart')
def daily_chart():

    #Reconnect to the DB
    connection = sqlite3.connect("plant_info.db")
    cursor = connection.cursor()

    #TODO - WRITE ACTUAL FUNCTION TO PREPARE DATA FOR CHARTING HERE
    #Fetch the last 30 entries of moisture data from the database and assign them to a variable
    cursor.execute("SELECT * FROM minute_reading ORDER BY date_time DESC LIMIT 1440")
    db_data = cursor.fetchall()  

    labels = []
    values = []

    # TODO - This is a pretty yuck way of handling the hourly view, ideally I implement an average of values, but I need to 
    # understand how to extract the hour from the timestamp, and catch any downtime on the ardiuno when times are not logged. 
    # This also needs to consider right now we're just grabbing the last 1440 values, and if there was downtime, they might be 
    # from another day if there is missing data. Currently just grabbing 1 value and assuming no downtime.
    for row in db_data:
        if row % 60 == True:
            values.append(row[1])

    for row in db_data:
        labels.append(row[0])
        values.append(row[1])

    # Close the connection
    connection.close()

    return render_template("graph.html", labels=labels, values=values)

    #fake = [{"percent" : 23, "box_colour" : "green"}]

    # Give data to the html
    #return render_template('index.html', monthly_moisture=monthly_moisture)
    #return render_template('index.html', monthly_moisture=map(to_model,rows))
    #print(list(map(to_model,rows)))
    return render_template('index.html', monthly_moisture=list(map(to_model,rows)))

box_colours_dict = {
    "wet-0" : "#F9E79F", 
    "wet-20" : "#F4D03F",
    "wet-40" : "#A3D77E",
    "wet-60": "#5D8B93",
    "wet-80": "#2471A3",
    "wet-100" : "#1D4E89"
}

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



def to_model(row):

    model = {
        "date_time" : row[0],
        "percent" : row[1],
        "box_colour" : row[2],
    }

    return model

