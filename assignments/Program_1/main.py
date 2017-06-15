import json
import os, sys
import pygame
import random
import math

# Get current working path
DIRPATH = os.path.dirname(os.path.realpath(__file__))


#####################################################################################
#####################################################################################

class Colors(object):
    """
    Opens a json file of web colors.
    """

    def __init__(self, file_name):

        with open(file_name, 'r') as content_file:
            content = content_file.read()

        self.content = json.loads(content)

    def get_random_color(self):
        """
        Returns a random rgb tuple from the color dictionary
        Args:
            None
        Returns:
            color (tuple) : (r,g,b)
        Usage:
            c = Colors()
            some_color = c.get_random_color()
            # some_color is now a tuple (r,g,b) representing some lucky color
        """
        r = random.randint(0, len(self.content) - 1)
        c = self.content[r]
        return (c['rgb'][0], c['rgb'][1], c['rgb'][2])

    def get_rgb(self, name):
        """
        Returns a named rgb tuple from the color dictionary
        Args:
            name (string) : name of color to return
        Returns:
            color (tuple) : (r,g,b)
        Usage:
            c = Colors()
            lavender = c.get_rgb('lavender')
            # lavender is now a tuple (230,230,250) representing that color
        """
        for c in self.content:
            if c['name'] == name:
                return (c['rgb'][0], c['rgb'][1], c['rgb'][2])
        return None

    def __getitem__(self, color_name):
        """
        Overloads "[]" brackets for this class so we can treat it like a dict.
        Usage:
            c = Colors()
            current_color = c['violet']
            # current_color contains: (238,130,238)
        """
        return self.get_rgb(color_name)


#####################################################################################
#####################################################################################

class StateBorders(object):
    """
    Opens a json file of the united states borders for each state.
    """

    def __init__(self, file_name):
        """
        Args:
            filename (string) : The path and filename to open
        Returns:
            None
        """
        with open(file_name, 'r') as content_file:
            content = content_file.read()

        self.content = json.loads(content)

    def get_state(self, name):
        """
        Returns a polygon of a single state from the US.
        Args:
            name (string): Name of a single state.

        Returns:
            json (string object): Json representation of a state

        Usage:
            sb = StateBorders()
            texas = sb.get_state_polygon('texas')
            # texas is now a list object containing polygons
        """
        for s in self.content:
            if s['name'].lower() == name.lower() or s['code'].lower() == name.lower():
                t = []
                for poly in s['borders']:
                    np = []
                    for p in poly:
                        np.append((p[0], p[1]))
                    t.append(np)
                return (t)

        return None

    def get_continental_states(self):
        """
        Returns a list of all the continental us states as polygons.
        Args:
            None

        Returns:
            list (list object): list of Json objects representing each continental state.

        Usage:
            sb = StateBorders()
            states = sb.get_continental_states()
            # states is now a list object containing polygons for all the continental states
        """
        states = []
        for s in self.content:
            t = []
            if s['name'] not in ['Alaska', 'Hawaii']:
                for poly in s['borders']:
                    np = []
                    for p in poly:
                        np.append((p[0], p[1]))
                    t.append(np)
                states.append(t)
        return (states)

    def key_exists(self, key):
        """
        Returns boolean if key exists in json
        Args:
            key (string) : some identifier

        Returns:
            T/F (bool) : True = Key exists
        """
        for s in self.content:
            if s['name'].lower() == key.lower():
                return True
            elif s['code'].lower() == key.lower():
                return True
        return False


#####################################################################################
#####################################################################################

class WorldCountries(object):
    """
    Opens a json file of the united states borders for each state.
    """

    def __init__(self, file_name):
        with open(file_name, 'r') as content_file:
            content = content_file.read()

        self.content = json.loads(content)

    def get_all_countries(self):
        """
        Returns a list of all the countries us states.
        Args:
            None

        Returns:
            list (list object): List of Json objects representing each country

        Usage:
            wc = WorldCountries()
            countries = wc.get_all_countries()
            # countries is now a list object containing polygons for all the countries
        """
        all_countries = []
        for c in self.content['features']:
            if c['id'] in ["ATA"]:
                continue
            all_countries.append(c['geometry']['coordinates'])
        return all_countries

    def get_country(self, id):
        """
        Returns a list of one country.
        Args:
            None

        Returns:
            list (list object): List of Json object representing a country

        Usage:
            wc = WorldCountries()
            country = wc.get_country('AFG')
            # country is now a list object containing polygons for 'Afghanistan'
        """
        country = []
        for c in self.content['features']:
            if c['id'].lower() == id.lower() or c['properties']['name'].lower() == id.lower():
                country.append(c['geometry']['coordinates'])
        return country

    def key_exists(self, key):
        """
        Returns boolean if key exists in json
        Args:
            key (string) : some identifier

        Returns:
            T/F (bool) : True = Key exists
        """
        for c in self.content['features']:
            if c['id'].lower() == key.lower():
                return True
            elif c['properties']['name'].lower() == key.lower():
                return True
        return False


#####################################################################################
#####################################################################################

class DrawGeoJson(object):
    __shared_state = {}

    def __init__(self, screen, width, height):
        """
        Converts lists (polygons) of lat/lon pairs into pixel coordinates in order to do some
        simple drawing using pygame.
        """
        self.__dict__ = self.__shared_state

        self.screen = screen  # window handle for pygame drawing

        self.polygons = []  # list of lists (polygons) to be drawn
        self.adjustedPolygons = [] # new var that holds polygons post adjustment

        self.all_lats = []  # list for all lats so we can find mins and max's
        self.all_lons = []

        self.mapWidth = width  # width of the map in pixels
        self.mapHeight = height  # height of the map in pixels
        self.mapLonLeft = -180.0  # extreme left longitude
        self.mapLonRight = 180.0  # extreme right longitude
        self.mapLonDelta = self.mapLonRight - self.mapLonLeft  # difference in longitudes
        self.mapLatBottom = 0.0  # extreme bottom latitude
        self.mapLatBottomDegree = self.mapLatBottom * math.pi / 180.0  # bottom in degrees

        self.colors = Colors(DIRPATH + '/../Json_Files/colors.json')

    def convertGeoToPixel(self, lon, lat):
        """
        Converts lat/lon to pixel within a set bounding box
        Args:
            lon (float): longitude
            lat (float): latitude

        Returns:
            point (tuple): x,y coords adjusted to fit on print window
        """
        x = (lon - self.mapLonLeft) * (self.mapWidth / self.mapLonDelta)

        lat = lat * math.pi / 180.0
        self.worldMapWidth = ((self.mapWidth / self.mapLonDelta) * 360) / (2 * math.pi)
        self.mapOffsetY = (self.worldMapWidth / 2 * math.log(
            (1 + math.sin(self.mapLatBottomDegree)) / (1 - math.sin(self.mapLatBottomDegree))))
        y = self.mapHeight - (
        (self.worldMapWidth / 2 * math.log((1 + math.sin(lat)) / (1 - math.sin(lat)))) - self.mapOffsetY)

        return (x, y)

    def add_polygon(self, poly):
        """
        Add a polygon to local collection to be drawn later
        Args:
            poly (list): list of lat/lons

        Returns:
            None
        """
        self.polygons.append(poly)
        for p in poly:
            x, y = p
            self.all_lons.append(x)
            self.all_lats.append(y)
        self.__update_bounds()

    def draw_polygons(self):
        """
        Draw our polygons to the screen
        Args:
            None

        Returns:
            None
        """
        self.adjustedPolygons = [] # clear list
        black = (0, 0, 0)
        for poly in self.polygons:
            adjusted = []
            for p in poly:
                x, y = p
                adjusted.append(self.convertGeoToPixel(x, y))
            self.adjustedPolygons.append(adjusted) # one liner added to fill adjusted polygons
            pygame.draw.polygon(self.screen, self.colors.get_random_color(), adjusted, 0)

    def draw_poly_outline(self, poly):
        """
        draws a black outline around a polygon
        Args:
            poly a list of (x,y) cords

        Returns:
            None
        """
        pygame.draw.polygon(self.screen, (0,0,0,), poly, 3)

    def __update_bounds(self):
        """
        Updates the "extremes" of all the points added to be drawn so
        the conversion to x,y coords will be adjusted correctly to fit
        the "bounding box" surrounding all the points. Not perfect.
        Args:
            None

        Returns:
            None
        """
        self.mapLonLeft = min(self.all_lons)
        self.mapLonRight = max(self.all_lons)
        self.mapLonDelta = self.mapLonRight - self.mapLonLeft
        self.mapLatBottom = min(self.all_lats)
        self.mapLatBottomDegree = self.mapLatBottom * math.pi / 180.0

    def __str__(self):
        return "[%d,%d,%d,%d,%d,%d,%d]" % (
        self.mapWidth, self.mapHeight, self.mapLonLeft, self.mapLonRight, self.mapLonDelta, self.mapLatBottom,
        self.mapLatBottomDegree)


#####################################################################################
#####################################################################################

class DrawingFacade(object):
    def __init__(self, width, height):
        """
        A facade pattern is used as a type of 'wrapper' to simplify interfacing with one or
        more other classes. This 'facade' lets us interface with the 3 classes instantiated
        below.
        """
        self.sb = StateBorders(DIRPATH + '/../Json_Files/state_borders.json')
        self.wc = WorldCountries(DIRPATH + '/../Json_Files/countries.geo.json')
        self.gd = DrawGeoJson(screen, width, height)

    def add_polygons(self, ids):
        """
        Adds polygons to the 'DrawGeoJson' class using country names or id's, state names or code's. It
        expects a list of values.
        Args:
            ids (list) : A list of any state or country identifiers

        Returns:
            None

        Usage:
            df.add_polygons(['FRA','TX','ESP','AFG','NY','ME','Kenya'])
        """
        for id in ids:
            if self.wc.key_exists(id):
                self.__add_country(self.wc.get_country(id))
            elif self.sb.key_exists(id):
                self.__add_state(self.sb.get_state(id))

    def __add_country(self, country):
        for polys in country:
            for poly in polys:
                if type(poly[0][0]) is float:
                    gd.add_polygon(poly)
                else:
                    for sub_poly in poly:
                        self.gd.add_polygon(sub_poly)

    def __add_state(self, state):
        for poly in state:
            self.gd.add_polygon(poly)


def create_bounding_box(poly):
    """
    creates a bounding box around a polygon
    :param poly:
    :return: none
    """
    minX = 1000
    minY = 1000
    maxX = 0
    maxY = 0
    for x,y in poly:
        if x < minX:
            minX = x
        if x > maxX:
            maxX = x
        if y < minY:
            minY = y
        if y > maxY:
            maxY = y
    pointList = [(minX,minY),(maxX,minY),(maxX,maxY),(minX,maxY)]
    pygame.draw.polygon(screen,(255,0,0),pointList,3)


def point_inside_polygon(x, y, poly):
    """
    determine if a point is inside a given polygon or not
    Polygon is a list of (x,y) pairs.
    http://www.ariel.com.au/a/python-point-int-poly.html
    """
    n = len(poly)
    inside = False

    p1x, p1y = poly[0]
    for i in range(n + 1):
        p2x, p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside


#####################################################################################
#####################################################################################

def mercator_projection(latlng, zoom=0, tile_size=256):
    """
    ******NOT USED******
    The mapping between latitude, longitude and pixels is defined by the web mercator projection.
    """
    x = (latlng[0] + 180) / 360 * tile_size
    y = ((1 - math.log(
        math.tan(latlng[1] * math.pi / 180) + 1 / math.cos(latlng[1] * math.pi / 180)) / math.pi) / 2 * pow(2,
                                                                                                            0)) * tile_size

    return (x, y)


if __name__ == '__main__':

    # every mouse down i placed in a mouse down x,y list
    # next we redraw
    # every draw we check if there is a x,y in the mousedown
    # remove x,y from list
    # draw the poly that click was in a second time no fill with black boarder

    # if there are no command line args
    if len(sys.argv) == 1:
        width = 1024  # define width and height of screen
        height = 512
    else:
        # use size passed in by user
        width = int(sys.argv[1])
        height = int(sys.argv[2])

    # create an instance of pygame
    # "screen" is what will be used as a reference so we can
    # pass it to functions and draw to it.
    screen = pygame.display.set_mode((width, height))

    # Set title of window
    pygame.display.set_caption('Draw World Polygons')

    # Set background to white
    screen.fill((255, 255, 255))

    # Refresh screen
    pygame.display.flip()

    # Instances of our drawing classes
    gd = DrawGeoJson(screen, width, height)
    df = DrawingFacade(width, height)

    # Add countries and states to our drawing facade.
    # df.add_polygons(['FRA','TX','ESP','AFG','NY'])
    # df.add_polygons(['TX','NY','ME','Kenya'])
    df.add_polygons(
        ['Spain', 'France', 'Belgium', 'Italy', 'Ireland', 'Scotland', 'Greece', 'Germany', 'Egypt', 'Morocco',
         'India'])

    # Main loop
    gd.draw_polygons()
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
                running = False
            # check for mouse down
            if event.type == pygame.MOUSEBUTTONDOWN:
                # clear screen
                screen.fill((255, 255, 255))
                # draw all the polygons again
                gd.draw_polygons()
                # get mouse location
                x,y = pygame.mouse.get_pos()
                # for all the adjusted polygons. these would be the true x,y cords
                for poly in gd.adjustedPolygons:
                    # test if the mouse was inside the polygon
                    if point_inside_polygon(x,y,poly):
                        # using the adjusted list draw a new polygon that is a black outline only
                        gd.draw_poly_outline(poly)
                        create_bounding_box(poly)
            pygame.display.flip()