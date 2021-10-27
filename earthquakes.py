# The Python standard library includes some functionality for communicating
# over the Internet.
# However, we will use a more powerful and simpler library called requests.
# This is external library that you may need to install first.
import requests


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
    
    with open("earthquakes.json", "w") as target:
        target.write(response.text)
    
    with open("earthquakes.json", "r") as json_file:
        my_data_as_string = json_file.read()
    
    mydata = json.loads(my_data_as_string)

    # We need to interpret the text to get values that we can work with.
    # What format is the text in? How can we load the values?
    
    return mydata

def count_earthquakes(data):
    """Get the total number of earthquakes in the response."""
    quake_count = data["metadata"]["count"]
    
    return quake_count

def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    magnitude = earthquake["properties"]["mag"]
    
    return magnitude

def get_location(earthquake):
    """Retrieve the latitude and longitude of an earthquake item."""
    # There are three coordinates, but we don't care about the third (altitude)
    x, y, z = earthquake["geometry"]["coordinates"]
    
    return f"coordinates: ({x}, {y})"

def get_maximum(data):
    """Get the magnitude and location of the strongest earthquake in the data."""
    
    featured_quakes = data["features"]
    
    strongest_quake = featured_quakes[0]
    max_magnitude = get_magnitude(strongest_quake)
    max_location = get_location(strongest_quake)
    
    for quake in featured_quakes:
        current_magnitude = get_magnitude(quake)
        if current_magnitude >= max_magnitude:
            strongest_quake = quake
            max_magnitude = current_magnitude
            max_location = get_location(quake)
    
    return max_magnitude, max_location

# With all the above functions defined, we can now call them and get the result
data = get_data()
print(f"Loaded {count_earthquakes(data)}")
max_magnitude, max_location = get_maximum(data)
print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}")