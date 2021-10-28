from datetime import date

import matplotlib.pyplot as plt
import requests
import json
import numpy as np

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

    # The response we get back is an object with several fields.
    # The actual contents we care about are in its text field:
    text = response.text
    # To understand the structure of this text, you may want to save it
    # to a file and open it in VS Code or a browser.
    # See the README file for more information.
    with open('earthquake.json', 'w') as data_file:
        data_file.write(text)

    # We need to interpret the text to get values that we can work with.
    # What format is the text in? How can we load the values?
    return json.loads(text)



def get_year(earthquake):
    """Extract the year in which an earthquake happened."""
    timestamp = earthquake['properties']['time']
    # The time is given in a strange-looking but commonly-used format.
    # To understand it, we can look at the documentation of the source data:
    # https://earthquake.usgs.gov/data/comcat/index.php#time
    # Fortunately, Python provides a way of interpreting this timestamp:
    # (Question for discussion: Why do we divide by 1000?)
    return date.fromtimestamp(timestamp/1000).year # milliseconds -> seconds


def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    return earthquake['properties']['mag']

# This is function you may want to create to break down the computations,
# although it is not necessary. You may also change it to something different.
def get_magnitudes_per_year(earthquakes):
    """
    Retrieve the magnitudes of all the earthquakes in a given year.
    Returns a dictionary with years as keys, and lists of magnitudes as values.
    """

    result = dict()
    for earthquake in earthquakes:
        year = get_year(earthquake)
        if year not in result:
            result[year] = np.array([get_magnitude(earthquake)])
        else:
            result[year] = np.append(result[year], get_magnitude(earthquake))
    
    return result


def plot_average_magnitude_per_year(earthquakes):
    result = get_magnitudes_per_year(earthquakes)
    average_magnitudes = [magnitudes.mean() for magnitudes in result.values() if len(magnitudes)]
    years = [year for year in result.keys() if len(result[year])]

    plt.plot(result.keys(), average_magnitudes)
    plt.show()


def plot_number_per_year(earthquakes):
    result = get_magnitudes_per_year(earthquakes)
    number_per_year = [len(magnitudes) for magnitudes in result.values()]
    
    plt.plot(result.keys(), number_per_year)
    plt.show()


# Get the data we will work with
quakes = get_data()['features']

# Plot the results - this is not perfect since the x axis is shown as real
# numbers rather than integers, which is what we would prefer!
plot_number_per_year(quakes)
plt.clf()  # This clears the figure, so that we don't overlay the two plots
plot_average_magnitude_per_year(quakes)
