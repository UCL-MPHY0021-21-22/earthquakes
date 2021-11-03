# The Python standard library includes some functionality for communicating
# over the Internet.
# However, we will use a more powerful and simpler library called requests.
# This is external library that you may need to install first.
import requests
import json
from datetime import date
import matplotlib.pyplot as plt

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
    # To understand the structure of this text, you may want to save it
    # to a file and open it in VS Code or a browser.
    # See the README file for more information.
    ...

    with open('text.json', 'w') as output_file:
        output_file.write(text)

    
    # We need to interpret the text to get values that we can work with.
    # What format is the text in? How can we load the values?
    return  json.loads(text)


def count_earthquakes(data):
    count = 0 
    for earthquake in data["features"]:
        if earthquake['properties']['type'] == 'earthquake':
            count+=1
    return count

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


def plot_number_per_year(earthquakes):
    years = []
    for earthquake in data["features"]:
        if earthquake['properties']['type'] == 'earthquake':
            years.append(get_year(earthquake))

    counts = {}

    for year in years:
        if year not in counts.keys():
            counts[year] = 1

        else:
            counts[year] += 1
    X, Y = zip(*counts.items()) #unzip the dictionary entries

    plt.plot(X,Y)
    plt.ylabel('Number of eathquakes')
    plt.xlabel('year')
    plt.show()

# This is function you may want to create to break down the computations,
# although it is not necessary. You may also change it to something different.

def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    return earthquake['properties']['mag']


def get_magnitudes_per_year(earthquakes):
    """Retrieve the magnitudes of all the earthquakes in a given year.
    
    Returns a dictionary with years as keys, and lists of magnitudes as values.
    """

    years = []
    mags = []

    for earthquake in data["features"]:
        if earthquake['properties']['type'] == 'earthquake':
            
            years.append(get_year(earthquake)) 
            mags.append(get_magnitude(earthquake))

    year_keys = set(years) #take unique years as keys
    magnitude_dic ={year:None for year in year_keys} # initialise the keys as unique years

    for unique_year in year_keys:
        mag_temp = []
        i = 0 
        for year in years:
            if unique_year == year:
                mag_temp.append(mags[i]) #take the magnitudes for this index
            magnitude_dic[unique_year] = mag_temp
            i+=1
    return magnitude_dic


def get_location(earthquake):
    """Retrieve the latitude and longitude of an earthquake item."""
    # There are three coordinates, but we don't care about the third (altitude)
    return earthquake['geometry']['coordinates'][:2]


def get_maximum(data):
    """Get the magnitude and location of the strongest earthquake in the data."""
    mags_per_year = get_magnitudes_per_year(data)
    max_mag = max(max(mags_per_year.values()))  #get the maximum magnitude 

    #find the corresponding location of that earthquake
    for earthquake in data["features"]:
            if earthquake['properties']['type'] == 'earthquake':
                if get_magnitude(earthquake) == max_mag:

                    max_location = get_location(earthquake)

    return max_mag,max_location

# With all the above functions defined, we can now call them and get the result
data = get_data()
print(f"Loaded {count_earthquakes(data)}")
max_magnitude, max_location = get_maximum(data)


print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}")