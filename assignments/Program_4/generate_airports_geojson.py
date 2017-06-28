import json
import pprint as p
import geo_helper as helper


# "00AK": {
#     "icao": "00AK",
#     "iata": "",
#     "name": "Lowell Field",
#     "city": "Anchor Point",
#     "country": "US",
#     "elevation": 450,
#     "lat": 59.94919968,
#     "lon": -151.695999146,
#     "tz": "America\/Anchorage"
# }

def convert_to_geo(data):
    # converted is a list of the finished stuff
    converted = []
    for key in data:
        element = data[key]
        geo_dict = helper.get_geo_format() # get empty shape
        geo_dict['geometry']['type'] = 'Point'
        geo_dict['geometry']['coordinates'] = (element['lon'],element['lat'])
        del element['lat']
        del element['lon']
        for k,v in element.items(): # create the properties from left over junk
            geo_dict['properties'][k] = v
        converted.append(geo_dict)
    return converted

if __name__ == '__main__':
    in_dir = 'WorldData/'
    in_file = 'airports'
    out_dir = 'geo_json/'
    out_file = 'airports'

    data = helper.read_json(in_dir+in_file)
    data = convert_to_geo(data)
    helper.create_geojson_file(data, out_dir + out_file)
