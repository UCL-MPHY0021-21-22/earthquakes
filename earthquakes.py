import requests
import json
from datetime import date
import numpy as np
import matplotlib.pyplot as plt

def get_data():
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
    data = json.loads(text)
    return data["features"]

def count_earthquakes(data):
    """Get the total number of earthquakes in the response."""
    return len(data)


def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    return earthquake["properties"]["mag"]


def get_location(earthquake):
    """Retrieve the latitude and longitude of an earthquake item."""
    return earthquake["geometry"]["coordinates"][0:2]


def get_maximum(data):
    """Get the magnitude and location of the strongest earthquake in the data."""
    mags = [get_magnitude(quake) for quake in data]
    max_value = max(mags)
    index = mags.index(max_value)
    return [max_value, get_location(data[index])]

def get_year(earthquake):
    """Gets the year from the given time format. 
    Uses attributes from the datetime."""
    timestamp = earthquake["properties"]["time"]
    return date.fromtimestamp(timestamp/1000).year

data = get_data()

# Defines arrays of the years of the earthquakes and empty arrays for the y plots.
years = np.arange(get_year(data[0]),get_year(data[-1]))
frequency = np.zeros(len(years))
av_mags = np.zeros(len(years))

#Loop counting the number of earthquakes per year
for earthquake in data:
    for indx, year in enumerate(years):
        if get_year(earthquake) == year:
            frequency[indx] +=1

#Loop working out the average magnitude per year, likely could be combined with the loop above
for indx, year in enumerate(years):
    mag = 0
    for earthquake in data:
        if get_year(earthquake) == year:
            mag += get_magnitude(earthquake)
    if frequency[indx] != 0:
        av_mags[indx] = mag/frequency[indx]
    else:
        av_mags[indx] = 0

#Plotting:
plot1 = plt.figure(1,figsize=(10,10))
plot1.add_subplot(2,1,1)
plt.bar(years,frequency,tick_label=years)
plt.xlabel("Year")
plt.ylabel("Frequency")
plt.title("Number of earthquakes per year")

plot1.add_subplot(2,1,2)
plt.plot(years,av_mags)
plt.xlabel("Year")
plt.ylabel("Average magnitude")
plt.title("Average magnitude of earthquakes per year")
plt.xticks(years)
plt.show()
plot1.savefig("earthquake_data.png")

# # With all the above functions defined, we can now call them and get the result
# print(f"Loaded {count_earthquakes(data)}")
# max_magnitude, max_location = get_maximum(data)
# print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}")