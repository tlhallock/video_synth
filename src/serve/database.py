"""DATABASE
MongoDB database initialization
"""

import pymongo

from .cfg import mongo_settings


client = pymongo.MongoClient(mongo_settings.uri)

db = client[mongo_settings.database]
project_collection: pymongo.collection = db[mongo_settings.project_collection]
thing_collection: pymongo.collection = db[mongo_settings.thing_collection]
videos_collection: pymongo.collection = db[mongo_settings.videos_collection]
arrays_collection: pymongo.collection = db[mongo_settings.arrays_collection]


videos_collection.create_index(
    [('path', pymongo.ASCENDING),],
    name='video_path_index',
    unique=True)

videos_collection.create_index(
    [('info.checksum', pymongo.HASHED),],
    name='video_checksum_index')

arrays_collection.create_index(
    [('path', pymongo.ASCENDING),],
    name='array_path_index',
    unique=True)

# arrays_collection.create_index(
#     [('variable_path', pymongo.ASCENDING),],
#     name='var_path_checksum_index')