"""DATABASE
MongoDB database initialization
"""

import pymongo

from .cfg import mongo_settings


client = pymongo.MongoClient(mongo_settings.uri)

db = client[mongo_settings.database]
project_collection: pymongo.collection = db[mongo_settings.project_collection]
thing_collection: pymongo.collection = db[mongo_settings.thing_collection]


# db.restaurants.create_index([('borough',pymongo.ASCENDING),
#                             ('cuisine',pymongo.ASCENDING)],
#                             name='borough_cuisine')