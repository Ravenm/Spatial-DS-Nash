import pprint as pretty
from pymongo import MongoClient
# Assumes state and airport are already a db collection

# create mongo connection
client = MongoClient() # default port
db = client.geo # db connection
states = db.states # collection in db
airports = db.airports

state = states.find_one()['loc']
# pretty.pprint(state)

query = airports.find({ "loc": {"$geoWithin": {"$geometry": state}}})

for result in query:
    pretty.pprint(result)
