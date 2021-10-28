# The Python standard library includes some functionality for communicating
# over the Internet.
# However, we will use a more powerful and simpler library called requests.
# This is external library that you may need to install first.
import requests
import json #for saving file to disk


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

def count_earthquakes(data):
    """Get the total number of earthquakes in the response."""
    #upon inspecting the JSON file, it is clear that the metadata ontains the count (120)
    return data["metadata"]["count"] #access metadata dictionary within data dictionary to find count key


def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    #We want to access the magnitude for a given earthquake
    return earthquake["properties"]["mag"]


def get_location(earthquake):
    """Retrieve the latitude and longitude of an earthquake item."""
    # There are three coordinates, but we don't care about the third (altitude)
    return earthquake["geometry"]["coordinates"][0:1]


def get_maximum(data):
    """Get the magnitude and location of the strongest earthquake in the data."""
    #extract magnitudes
    mags = [get_magnitude(earthquakes) for earthquakes in data]
    #find maximum magnitude
    max_magnitude = max(mags)
    mag_index = mags.index( max_magnitude)
    #get locations list
    locs = [get_location(earthquakes) for earthquakes in data]
    max_location = locs[mag_index]
    return [max_magnitude, max_location]


# With all the above functions defined, we can now call them and get the result
data = get_data()
print(f"Loaded {count_earthquakes(data)}")
max_magnitude, max_location = get_maximum(data)
print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}")