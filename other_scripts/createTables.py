from pymongo import MongoClient

client = MongoClient()
db = client.test_database
sessionID = 'test'

try:
    track_collection = db['track_collection_test']
    progress_collection = db['progress_collection_test']
    agg_collection = db['agg_collection_test']

    progress_collection.insert_one({
        'sal': 'cf'
    })

    agg_collection.insert_one({
        'o': 'nu'
    })
except:
    print('Pula mea...')
