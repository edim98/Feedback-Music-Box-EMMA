'''
Helper module for dropping collections from the database.
'''

from pymongo import MongoClient

client = MongoClient()
db = client.test_database
sessionID = 'test'

try:
    db['agg_collection_test'].drop()
except:
    print('Cant drop collection agg_collection...')


try:
    db['progress_collection_test'].drop()
except:
    print('Cant drop collection progress_collection...')

try:
    db['track_collection_test'].drop()
except:
    print('Cant drop collection track_collection...')