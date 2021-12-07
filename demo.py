# The Python standard library includes some functionality for communicating
# over the Internet.
# However, we will use a more powerful and simpler library called requests.
# This is external library that you may need to install first.
import requests
import json



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

# print(response.text)

# Download all the data
with open('downloaded.json','w') as output_file:
    output_file.write(response.text)



# Check the data type
data = json.loads(response.text)
print(type(data))
for key in data:
    print(key)

# 
with open('rewritten.json', 'w') as new_output_file:
    json.dump(data, new_output_file)
