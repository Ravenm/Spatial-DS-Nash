import pprint as pretty
from pymongo import MongoClient


# create mongo connection
client = MongoClient() # default port
db = client.geo # db connection
states = db.states # collection in db
airports = db.airports

# pretty.pprint(airports.find_one())

