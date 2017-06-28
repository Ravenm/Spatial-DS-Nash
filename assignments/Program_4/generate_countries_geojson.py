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
    # hue hue hue hue
    return data['features']

if __name__ == '__main__':
    in_dir = 'WorldData/'
    in_file = 'countries.geo'
    out_dir = 'geo_json/'
    out_file = 'countries'

    data = helper.read_json(in_dir+in_file)
    data = convert_to_geo(data)
    helper.create_geojson_file(data, out_dir + out_file)
