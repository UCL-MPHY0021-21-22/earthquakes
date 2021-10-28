from datetime import date
import requests
import json
import numpy as np

import matplotlib.pyplot as plt


def get_data():
    """Retrieve the data we will be working with."""
    # With requests, we can ask the web service for the data.
    # Can you understand the parameters we are passing here?
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

    # The response we get back is an object with several fields.
    # The actual contents we care about are in its text field:
    text = response.text

    # Loading the text as a dictionary using json
    return json.loads(text)


def get_year(earthquake):
    """Extract the year in which an earthquake happened."""
    timestamp = earthquake['properties']['time']
    # The time is given in a strange-looking but commonly-used format.
    # To understand it, we can look at the documentation of the source data:
    # https://earthquake.usgs.gov/data/comcat/index.php#time
    # Fortunately, Python provides a way of interpreting this timestamp:
    #  timestamp is in ms and fromtimestamp takes s so divide by 1000
    year = date.fromtimestamp(timestamp/1000).year
    return year


def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    return earthquake["properties"]["mag"]


# This is function you may want to create to break down the computations,
# although it is not necessary. You may also change it to something different.
def get_magnitudes_per_year(earthquakes):
    res = {}
    for quake in earthquakes:
        year = get_year(quake)
        mag = get_magnitude(quake)
        if year not in res.keys():
            res[year] = [mag]
        else:
            res[year].append(mag)
    """Retrieve the magnitudes of all the earthquakes in a given year.
    
    Returns a dictionary with years as keys, and lists of magnitudes as values.
    """
    return res


def plot_average_magnitude_per_year(earthquakes):
    mag_per_year = get_magnitudes_per_year(earthquakes)
    list_year =  mag_per_year.keys()
    ## If we want it to be a numpy array
    # list_year = np.array(list(mag_per_year.keys()))
    list_av_mag = [sum(mags)/len(mags) for mags in mag_per_year.values()]

    plt.plot(list_year, list_av_mag)
    plt.xlabel("Year")
    plt.ylabel("Average magnitude")
    plt.title("Average magnitude of earthquakes per year")
    plt.show()


def plot_number_per_year(earthquakes):
    mag_per_year = get_magnitudes_per_year(earthquakes)
    list_year = mag_per_year.keys()
    list_number = [len(mags) for mags in mag_per_year.values()]

    plt.plot(list_year, list_number)
    plt.xlabel("Year")
    plt.ylabel("Number")
    plt.title("Number of earthquakes per year")
    plt.show()

def plot_number_and_average_magnitude_per_year(earthquakes):
    mag_per_year = get_magnitudes_per_year(earthquakes)
    list_year = mag_per_year.keys()
    list_number = np.array([len(mags) for mags in mag_per_year.values()])
    list_av_mag = np.array([sum(mags) for mags in mag_per_year.values()])/list_number

    plt.plot(list_year, list_number, ls = '--', label = "Number")
    plt.plot(list_year, list_av_mag, label = "Average magnitude")
    # Put the x-axis as integer years 
    plt.xticks(np.linspace(min(list_year), max(list_year), (max(list_year)-min(list_year))//2+1))
    plt.xlabel("Year")
    plt.title("Magntiude and number of earthquakes per year")
    plt.legend()
    plt.show()


# Get the data we will work with
quakes = get_data()['features']

# Plot the results - this is not perfect since the x axis is shown as real
# numbers rather than integers, which is what we would prefer!
plot_number_per_year(quakes)
plt.clf()  # This clears the figure, so that we don't overlay the two plots
plot_average_magnitude_per_year(quakes)
plt.clf()
plot_number_and_average_magnitude_per_year(quakes)