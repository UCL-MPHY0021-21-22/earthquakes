import requests
import json

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



# With all the above functions defined, we can now call them and get the result
data = get_data()
print(f"Loaded {count_earthquakes(data)}")
max_magnitude, max_location = get_maximum(data)
print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}")