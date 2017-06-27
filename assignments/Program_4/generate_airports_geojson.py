import json

def read_json(file):
    with open(file, 'r') as f:
        return f.readlines()


def create_geojson_file(data, file):
    with open(file + '.geojson', 'w') as f:
        f.writelines(json.dumps(data))


def get_geo_format():
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
