import pprint as pretty
import csv
import os, sys
import pygame
import random


DIRPATH = os.path.dirname(os.path.realpath(__file__))
keys = []
key_found = False

def _adjust_location_cords(points):
    maxx = float(1067226) # The max coords from the
    maxy = float(271820) # whole file
    minx = float(913357)
    miny = float(121250)
    deltax = float(maxx) - float(minx)
    deltay = float(maxy) - float(miny)

    adjusted_points = []
    #pretty.pprint(points)
    for p in points:
        x,y = p
        x = float(x)
        y = float(y)
        xprime = (x - minx) / deltax     # val (0,1)
        yprime = 1.0 - ((y - miny) / deltay) # val (0,1)
        # pretty.pprint((xprime,yprime))
        adjusted_points.append((int(xprime*1000),int(yprime*1000)))
    # pretty.pprint(adjusted_points)
    return adjusted_points


def read_json(file_name):
    with open(DIRPATH + "/NYPD_CrimeData/" + file_name) as f:
        return csv.DictReader(f)


def draw_points(file_name, color, screen):
    global key_found
    global keys
    crimes = []
    points = []
    with open(DIRPATH + "/NYPD_CrimeData/" + file_name) as f:
        for line in f:
            line = ''.join(x if i % 2 == 0 else x.replace(',', ':') for i, x in enumerate(line.split('"')))
            line = line.strip().split(',')
            if not key_found:
                keys = line
                key_found = True
                continue
            crimes.append(line)
        xcord = keys.index('X_COORD_CD')
        ycord = keys.index('Y_COORD_CD')

        # pretty.pprint(keys)

        for row in crimes:
            if row[xcord] and row[ycord]:
                points.append((row[xcord],row[ycord]))

        for x,y in _adjust_location_cords(points):
            pygame.draw.circle(screen,color,(x,y),1,1)


def print_bronx(screen):
    file_name = "filtered_crimes_bronx.csv"
    color = (2,120,120)
    draw_points(file_name,color,screen)


def print_brooklyn(screen):
    file_name = "filtered_crimes_brooklyn.csv"
    color = (128,22,56)
    draw_points(file_name,color,screen)


def print_manhattan(screen):
    file_name = "filtered_crimes_manhattan.csv"
    color = (194,35,38)
    draw_points(file_name,color,screen)


def print_queens(screen):
    file_name = "filtered_crimes_queens.csv"
    color = (243,115,56)
    draw_points(file_name,color,screen)


def print_staten_island(screen):
    file_name = "filtered_crimes_staten_island.csv"
    color = (253,182,50)
    draw_points(file_name,color,screen)


def draw_label():
    pygame.font.init()  # you have to call this at the start,
    # if you want to use this module.
    my_font = pygame.font.SysFont('Arial', 30)

    text_surface = my_font.render('Program 2A', False, (0, 0, 0))

    screen.blit(text_surface, (0, 0))

    text_surface = my_font.render('Andrew Nash', False, (0, 0, 0))

    screen.blit(text_surface, (0, 40))


if __name__ == '__main__':

    width = 1000
    height = 1000
    screen = pygame.display.set_mode((width, height))

    # Set title of window
    pygame.display.set_caption('NY Crimes')

    # Set background to white
    screen.fill((255, 255, 255))

    # Refresh screen
    pygame.display.flip()

    print_bronx(screen)
    print_brooklyn(screen)
    print_manhattan(screen)
    print_queens(screen)
    print_staten_island(screen)

    draw_label()

    pygame.display.flip()

    running = True
    while running:
        # gd.draw_polygons()
        # added one line of code, one new var, and a new method
        # code added to draw_polygons in DrawGeoJson to capture polygon x,y after adjustment
        # new var located in DrawGeoJson adjustedPolygons is a list of post adjustment polygons
        # new method located in DrawGeoJson draw_poly_outline takes a polygons x,y list and draws an outline
        # add dictionary to hold name and color for redraw

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.image.save(screen, 'all_buroughs_screen.png')
                running = False
