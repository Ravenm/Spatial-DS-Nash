import json
import pprint as p
import geo_helper as helper

# {
#     "Altitude": "641",
#     "Country": "Honshu-Japan",
#     "Lat": "34.5",
#     "Lon": "131.6",
#     "Name": "Abu",
#     "Type": "Shield volcanoes"
# }


def convert_to_geo(data):
    converted = []
    for element in data:
        geo_dict = get_geo_format()
        geo_dict['geometry']['type'] = 'Point'
        geo_dict['geometry']['coordinates'] = (element['Lon'],element['Lat'])
        del element['Lat']
        del element['Lon']
        for k,v in element.items():
            geo_dict['properties'][k] = v
        converted.append(geo_dict)
    return converted

if __name__ == '__main__':
    in_dir = 'WorldData/'
    in_file = 'world_volcanos'
    out_dir = 'geo_json/'
    out_file = 'volcanos'

    data = helper.read_json(in_dir+in_file)
    data = convert_to_geo(data)
    helper.create_geojson_file(data, out_dir + out_file)
