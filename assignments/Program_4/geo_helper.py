import json
import pprint as p


def read_json(file):
    # read in a json file as json return json
    with open(file + '.json', 'r') as f:
        return json.load(f)


def create_geojson_file(data, file):
    del data[999:len(data)-1]
    with open(file + '.geojson', 'w') as f:
        f.writelines(json.dumps(data, indent=4, sort_keys=False))


def get_geo_format():
    # create a base shape for output
    #       "type": "Feature",
    #       "properties": {
    #       },
    #       "geometry": {
    #         "type": "",
    #         "coordinates": [
    #         ]
    #       }
    #     }
    foo = {'type': 'Feature', 'properties': {}, 'geometry': {}}
    foo['geometry']['type'] = ''
    foo['geometry']['coordinates'] = []
    return foo

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