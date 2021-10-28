from earthquakes import get_data

from datetime import date

import matplotlib.pyplot as plt
import numpy as np

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
    magnitude = earthquake['properties']['mag']

    return magnitude


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
    years = []
    for i in quakes:
        years.append(get_year(i))
    
    plt.hist(years, np.arange(1999.5,2019.5,1))
    plt.title('Earthquake Frequency')
    plt.xlabel('Year')
    plt.ylabel('Frequency(Number)')
    plt.show()



# Get the data we will work with
quakes = get_data()['features']

# Plot the results - this is not perfect since the x axis is shown as real
# numbers rather than integers, which is what we would prefer!
plot_number_per_year(quakes)
#plt.clf()  # This clears the figure, so that we don't overlay the two plots
#plot_average_magnitude_per_year(quakes)