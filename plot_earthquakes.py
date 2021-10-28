from datetime import date
import requests
import numpy as np
import matplotlib.pyplot as plt
import json
import pandas
import collections


def get_data():
    """Retrieve the data we will be working with."""
    response = requests.get(
        "http://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
        params={
            'starttime': "2000-01-01",
            "maxlatitude": "58.723",
            "minlatitude": "50.008",
            "maxlongitude": "1.67",
            "minlongitude": "-9.756",
            "minmagnitude": "1",
            "endtime": "2018-10-11",
            "orderby": "time-asc"}
    )

    mydata = json.loads(response.text)
    
    return mydata
    
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
    ...

# This is function you may want to create to break down the computations,
# although it is not necessary. You may also change it to something different.
def get_magnitudes_per_year(earthquakes):
    """Retrieve the magnitudes of all the earthquakes in a given year.
    
    Returns a dictionary with years as keys, and lists of magnitudes as values.
    """
    ...

def plot_average_magnitude_per_year(earthquakes):
    ...

def plot_number_per_year(earthquakes):
    list_of_years = [get_year(quake) for quake in quakes]
    
    counter = collections.Counter(list_of_years)
    
    labels = counter.values()
    
    count = counter.keys()

    fig, ax = plt.subplots()

    ax.bar(count, labels, label='Earthquakes')

    ax.set_ylabel('Earthquake count')
    ax.set_title('Earthquakes per year')

    plt.show()
    
# Get the data we will work with
quakes = get_data()['features']

# Plot the results - this is not perfect since the x axis is shown as real
# numbers rather than integers, which is what we would prefer!
plot_number_per_year(quakes)
# plt.clf()  # This clears the figure, so that we don't overlay the two plots
# plot_average_magnitude_per_year(quakes)
