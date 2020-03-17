'''
Store a session's aggregated data.
'''
import time

from app import track_history
from app import progress_history

def create_agg_log(db, sessionID):
    collection_name = 'agg_collection_' + sessionID
    agg_collection = db[collection_name]
    return agg_collection

def update_agg_log(db, sessionID, trackID, end_status='normal', song_score=0):

    agg_collection = db['agg_collection_' + sessionID]

    start_timestamp = track_history.get_track_info(db, sessionID, trackID)['timestamp']

    try:
        end_timestamp = track_history.get_track_log(db, sessionID, start=start_timestamp)[0]['timestamp']
    except:
        end_timestamp = time.time()

    log = progress_history.get_progress_trend(db, sessionID, start=start_timestamp, end=end_timestamp)

    try:
        agg_collection.insert_one({
            'start': start_timestamp,
            'end': end_timestamp,
            'trackID': trackID,
            'end_status': end_status,
            'song_score': song_score,  # TO DO
            'agg_prog_log': log
        })
    except:
        print('Unable to update collection: agg_collection!')

def delete_agg_log(db, sessionID):
    collection_name = 'agg_collection_' + sessionID
    try:
        db[collection_name].drop()
    except:
        print('Could not drop collection: agg_collection!')

def get_agg_log(db, sessionID, start='', end=''):
    agg_collection = db['agg_collection_' + sessionID]

    result = []

    if start == '':
        start = 0.0
    if end == '':
        end = time.time()

    query = agg_collection.find({
        '$and': [
            {'start': {'$gt': start}},
            {'start': {'$lt': end}}
        ]
    })

    for entry in query:
        result.append(entry)

    return result

