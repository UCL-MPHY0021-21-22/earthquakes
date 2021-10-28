from datetime import date
import requests
import matplotlib.pyplot as plt
import json

import pandas as pd


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

    text = response.text
    return json.loads(text)


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
    years = []
    magnitudes = []
    for earthquake in earthquakes:

        years.append(get_year(earthquake))
        magnitudes.append(get_magnitude(earthquake))
    
    quake_dictionary = dict(zip(years, magnitudes))
    
    year_count = pd.value_counts(years)
    year_count = year_count.sort_index()
    return year_count
    
    
    
def plot_average_magnitude_per_year(earthquakes):
    year_count = get_magnitudes_per_year(earthquakes)
    
    years = list(year_count.index)
    frequency = year_count.tolist()
    
    
    
    fig = plt.plot()
    plt.bar(years, frequency)
    plt.xticks(years, years, rotation='vertical')
    plt.show
    
    
    
quakes = get_data()['features']
plot_average_magnitude_per_year(quakes)