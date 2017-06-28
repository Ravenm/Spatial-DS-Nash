import json
import pprint as p
import geo_helper as helper


# {"name": "Wyoming", "code": "wy", "borders":
#   [
#       [
#           [-111.137695, 45.026951],
#           [-104.029541, 45.034710],
#           [-104.040527, 40.996483],
#           [-111.115723, 40.979897],
#           [-111.137695, 45.026951]
#       ]
#   ]
# }


def convert_to_geo(data):
    # empty list to hold junk
    converted = []
    for key in data:
        list = data[key]
        for element in list:
            geo_dict = helper.get_geo_format()
            geo_dict['geometry']['type'] = 'Point'
            # base file holds info in a weird way dict dict list
            geo_dict['geometry']['coordinates'] = (element['geometry']['coordinates'][0],
                                                   element['geometry']['coordinates'][1])
            del element['geometry']
            for k,v in element.items():
                geo_dict['properties'][k] = v # left overs are for properties
            converted.append(geo_dict)
    return converted

if __name__ == '__main__':
    in_dir = 'WorldData/'
    in_file = 'earthquakes-1960-2017'
    out_dir = 'geo_json/'
    out_file = 'earthquakes'

    data = helper.read_json(in_dir+in_file)
    data = convert_to_geo(data)
    helper.create_geojson_file(data, out_dir + out_file)
