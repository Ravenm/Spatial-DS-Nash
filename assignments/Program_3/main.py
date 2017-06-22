import pygame
from pygame.locals import *
import math
import json
import os
import pprint
import requests


def get_quake_data(year, month=[1, 12], minmag=7, maxmag=None, query=True):
    start_month = month[0]
    end_month = month[1]

    if not maxmag is None:
        maxmag = '&maxmagnitude=' + str(maxmag)
    else:
        maxmag = ''

    if not minmag is None:
        minmag = '&minmagnitude=' + str(minmag)
    else:
        minmag = '&minmagnitude=' + str(1.0)

    if query:
        type = 'query'

    else:
        type = 'count'

    url = 'https://earthquake.usgs.gov/fdsnws/event/1/' + type + '?format=geojson&starttime=' + str(
        year[0]) + '-' + str(start_month) + '-01&endtime=' + str(year[1]) + '-' + str(end_month) + '-01' + minmag + maxmag

    r = requests.get(url).json()

    if type == 'count':
        return r['count']
    else:
        return r


def condense_data(data):
    condensed_data = []

    for quake in data['features']:
        keep = {'geometry': quake['geometry'], 'mag': quake["properties"]["mag"],
                'magType': quake["properties"]["magType"], 'time': quake["properties"]["time"],
                'place': quake["properties"]["place"], 'types': quake["properties"]["types"],
                'rms': quake["properties"]["rms"], 'sig': quake["properties"]["sig"]}
        condensed_data.append(keep)

    return condensed_data


def create_json(r, file_name):
    with open(file_name + '.json', 'w+') as f:
        f.write(json.dumps(r, sort_keys=True, indent=4, separators=(',', ': ')))


def merc_x(lon, zoom=1):
    lon = math.radians(lon)
    a = (256 / math.pi) * 2
    b = lon + math.pi
    return int(a * b)


def merc_y(lat, zoom=1):
    zoom = 1.0
    lat = math.radians(lat)
    a = (256.0 / math.pi) * pow(2.0, zoom)
    b = abs(math.tan(math.pi / 4 + lat / 2))
    if not b:
        b = .01
    c = math.pi - math.log(b)

    return int(a * c)


def adjust_location_coords(data, width, height):
    """
    Adjust your point data to fit in the screen.
    Input:
        extremes: dictionary with all maxes and mins
        points: list of points
        width: width of screen to plot to
        height: height of screen to plot to
    """
    data['adj'] = []
    maxx = float(data['maxX']) # The max coords from bounding rectangles
    minx = float(data['minX'])
    maxy = float(data['maxY'])
    miny = float(data['minY'])
    deltax = float(maxx) - float(minx)
    deltay = float(maxy) - float(miny)

    for p in data['points']:
        x,y = p
        x = float(x)
        y = float(y)
        xprime = (x - minx) / deltax         # val (0,1)
        yprime = ((y - miny) / deltay)  # val (0,1)
        adjx = int(xprime*width)
        adjy = int(yprime*height)
        data['adj'].append((adjx,adjy))

    return data


def translate(data):
    allx = []
    ally = []
    newData = {'points': [], 'mag': [], 'allx': [], 'ally': []}
    # Loop through converting lat/lon to x/y and saving extreme values.
    for quake in data:
        # st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        lon = quake['geometry']['coordinates'][0]
        lat = quake['geometry']['coordinates'][1]
        x, y = (merc_x(lon), merc_y(lat))
        newData['allx'].append(x)
        newData['ally'].append(y)
        newData['points'].append((x, y))
        newData['mag'].append(quake['mag'])
    return newData


def _draw(data):

    for quake in range(len(data['adj'])):

        x, y = data['adj'][quake]

        mag = pow(10, data['mag'][quake])
        mag = math.sqrt(mag)
        # print('point: %d, %d  mag: %d', (x,y,mag))
        OldRange = (math.sqrt(pow(10, 10)))
        NewRange = (120 - 100)
        NewValue = (((mag - 0) * NewRange) / OldRange)
        print(NewValue)
        pygame.draw.circle(screen, (0, 255, 0), (x, y), int(NewValue) + 2)
        pygame.display.flip()


if __name__ == '__main__':

    year = [1960, 2017]
    month = [1, 12]
    minMag = 7
    quakes = {}

    width = 1024
    height = 512
    screen = pygame.display.set_mode((width, height))

    img = pygame.image.load('1024x512.bmp')

    white = (255, 64, 64)
    screen.fill((white))
    running = 1
    screen.blit(img, (0, 0))
    pygame.display.flip()

    remoteData = get_quake_data(year)
    create_json(remoteData,'quake_data')
    condenseData = condense_data(remoteData)
    create_json(condenseData, 'quake_data_condensed')

    quakes = translate(condenseData)


    quakes['maxX'] = max(quakes['allx'])
    quakes['minX'] = min(quakes['allx'])
    quakes['maxY'] = max(quakes['ally'])
    quakes['minY'] = min(quakes['ally'])

    quakes = adjust_location_coords(quakes, width, height)

    _draw(quakes)

    # with open('quake_data.json') as data_file:
    #     data = json.load(data_file)

    # for location in data:
    #     lat = int(location['geometry']['coordinates'][0])
    #     lon = int(location['geometry']['coordinates'][1])
    #
    #     # print('break')
    #     # print(lat)
    #     # print(lon)
    #
    #     mag = location['mag']
    #     _draw(lat, lon, mag)
    #     pygame.display.flip()
    #
    # # draw(-20.7303, -176.4767, 7)
    # # pygame.display.flip()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.image.save(screen, 'quake_data.png')
                running = False
                # if event.type == pygame.MOUSEBUTTONDOWN:
                #     screen.fill((white))
                #     screen.blit(img, (0, 0))
                #     pygame.display.flip()
