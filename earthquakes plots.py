# The Python standard library includes some functionality for communicating
# over the Internet.
# However, we will use a more powerful and simpler library called requests.
# This is external library that you may need to install first.
import requests
import json #for saving file to disk
from datetime import date
import matplotlib.pyplot as plt
import numpy as np


def get_data():
    # With requests, we can ask the web service for the data.
    # Can you understand the parameters we are passing here?
    response = requests.get(
        "http://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
        params={
            'starttime': "2000-01-01", #beginning date of query
            #Use a rectangle to cover the map (min-max lat and min-max long)
            "maxlatitude": "58.723", #UK maximum latitude to query
            "minlatitude": "50.008", #UK minimum latitude to query
            "maxlongitude": "1.67", #Upper value of UK longitude to query
            "minlongitude": "-9.756", #Lower value of UK longtitude to query
            "minmagnitude": "1", #Looking for earthquakes with a higher magnitude than 1
            "endtime": "2018-10-11", #End of date range we are looking into
            "orderby": "time-asc"} #want time ascending dates
        
    )

    # The response we get back is an object with several fields.
    # The actual contents we care about are in its text field:
    text = response.text
    
    #write to a json file
    with open('earthquakes_data.json', 'w') as earthquakes_data_out:
        earthquakes_data_out.write(json.dumps(text,indent=4))
        
    #parse text variable using json loads
    data = json.loads(text)
    return data

def get_year(earthquake):
    """Extract the year in which an earthquake happened."""
    timestamp = earthquake['properties']['time']
    # The time is given in a strange-looking but commonly-used format.
    # To understand it, we can look at the documentation of the source data:
    # https://earthquake.usgs.gov/data/comcat/index.php#time
    # Fortunately, Python provides a way of interpreting this timestamp:
    # (Question for discussion: Why do we divide by 1000?)
    year = date.fromtimestamp(timestamp/1000).year
    return year


def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    magnitude = earthquake["properties"]["mag"]
    return magnitude


# This is function you may want to create to break down the computations,
# although it is not necessary. You may also change it to something different.
def get_magnitudes_per_year(earthquakes):
    """Retrieve the magnitudes of all the earthquakes in a given year.
    
    Returns a dictionary with years as keys, and lists of magnitudes as values.
    """
    #initialise dictionary
    magnitudes_per_year = {}
    for key in range(len(earthquakes)):
        year = get_year(earthquakes[key])
        mag = get_magnitude(earthquakes[key])
        #see if current element is already a key, if so append value to list
        if year in magnitudes_per_year:    
            magnitudes_per_year[year].append(mag)
        else: #create new year key
            magnitudes_per_year[year] = [mag]
    return magnitudes_per_year


def plot_average_magnitude_per_year(earthquakes):
    #find the magnitudes per year
    magnitudes_per_year = get_magnitudes_per_year(earthquakes)
    years = list(magnitudes_per_year.keys())
    avg_magnitudes = []
    for key in range(len(magnitudes_per_year)):
        magnitudes = magnitudes_per_year[key]
        #calculate mean
        avg_magnitudes.append(np.mean(magnitudes))
    plt.plot(years,avg_magnitudes)
        
    ...


def plot_number_per_year(earthquakes):
    ...



# Get the data we will work with
quakes = get_data()['features']
#
# Plot the results - this is not perfect since the x axis is shown as real
# numbers rather than integers, which is what we would prefer!
plot_number_per_year(quakes)
plt.clf()  # This clears the figure, so that we don't overlay the two plots
plot_average_magnitude_per_year(quakes)