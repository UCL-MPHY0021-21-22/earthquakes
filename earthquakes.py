# The Python standard library includes some functionality for communicating
# over the Internet.
# However, we will use a more powerful and simpler library called requests.
# This is external library that you may need to install first.
import requests
import os # The 'os' module gives us all the tools we need to search in the file system

os.getcwd() # Use the 'getcwd' function from the 'os' module to find where we are on disk.
import json

def get_data():
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
    with open("downloaded.json", "w") as output_file:
        output_file.write(response.text)
    data = json.loads(response.text)
    print(type(data))
    for key in data:
        print(key)
    #with open("rewritten.json", "w") as new_output_file:
    #    json.dump(data, new_output_file)

    # To understand the structure of this text, you may want to save it
    # to a file and open it in VS Code or a browser.
    # See the README file for more information.
    ...

    # We need to interpret the text to get values that we can work with.
    # What format is the text in? How can we load the values?
    return data

def count_earthquakes(data):
    return data.get("metadata").get("count")


def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    return [dict.get("properties").get("mag") for dict in data.get("features")]


def get_location(earthquake):
    """Retrieve the latitude and longitude of an earthquake item."""
    # There are three coordinates, but we don't care about the third (altitude)
    list_of_coords = [dict.get("geometry").get("coordinates") for dict in data.get("features")]
    lat_lon_only = [coords[0:2] for coords in list_of_coords]
    return lat_lon_only


def get_maximum(data):
    """Get the magnitude and location of the strongest earthquake in the data."""
    mag_lat_lon = sorted([(([dict.get("properties").get("mag")]+dict.get("geometry").get("coordinates"))[0:3]) for dict in data.get("features")], reverse = True)
    max_magnitude = mag_lat_lon[0][0]
    max_location = mag_lat_lon[0][1:3]
    return max_magnitude, max_location

# With all the above functions defined, we can now call them and get the result
data = get_data()

print(f"Loaded {count_earthquakes(data)}")
max_magnitude, max_location = get_maximum(data)
print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}")


############################################################################################
############################################################################################

#the frequency (number) of earthquakes per year

import matplotlib.pyplot as plt
import numpy as np

import datetime
time_humanfriendly = [datetime.datetime.fromtimestamp((dict.get("properties").get("time"))/1000).strftime('%Y') for dict in data.get("features")]
x = time_humanfriendly

plt.xticks(rotation = 'vertical')
plt.hist(x, density=False)  
plt.ylabel('Count of Earthquakes')
plt.xlabel('Years')
plt.show()
plt.savefig('frequency_per_year.png');

############################################################################################
############################################################################################

#the average magnitude of earthquakes per year

import pandas as pd

magnitude_and_years = [(  [dict.get("properties").get("mag")]   +   [datetime.datetime.fromtimestamp((dict.get("properties").get("time"))/1000).strftime('%Y')]  ) for dict in data.get("features")]
magnitude_and_years

mag_years_df = pd.DataFrame(magnitude_and_years, columns=["magnitude","years"])
mag_years_df_grouped = mag_years_df.groupby(["years"]).mean()
mag_years_df_grouped.plot(kind = "bar").figure.savefig('magnitude_per_year.png')