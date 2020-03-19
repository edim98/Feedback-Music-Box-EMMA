"""
Store a session's track history.
"""

import time

def create_track_log(db, sessionID):
    """
    Instantiate the Track History Collection.
    :param db: The database object.
    :param sessionID: Current user's session ID.
    :return: The Track History Collection object.
    """

    collection_name = 'track_collection_' + sessionID
    track_collection = db[collection_name]
    return track_collection

def update_track_log(db, sessionID, trackID):
    """
    Add new track entries in the Track History Collection.
    :param db: The database object.
    :param sessionID: Current user's session ID.
    :param trackID: Current track's ID.
    :return: Nothing.
    """

    track_collection = db['track_collection_' + sessionID]

    try:
        track_collection.insert_one({
            "timestamp" : time.time(),
            "trackID" : trackID
        })
    except:
        print('Unable to update collection: track_collection!')

def delete_track_log(db, sessionID):
    """
    Drop the Track History Collection.
    :param db: The database object.
    :param sessionID: Current user's session ID.
    :return: Nothing.
    """

    collection_name = 'track_collection_' + sessionID
    try:
        db[collection_name].drop()
    except:
        print('Could not drop collection: track_collection!')


def get_track_info(db, sessionID, trackID):
    """
    Query the Collection for a given song.
    :param db: The database object.
    :param sessionID: Current user's session ID.
    :param trackID: The song's unique identifier.
    :return: Collection entry matching the query.
    """

    track_collection = db['track_collection_' + sessionID]

    try:
        query = track_collection.find_one({
            'trackID': trackID
        })
    except:
        print('Error querying collection: track_collection!')

    return query

def get_track_log(db, sessionID, start = '', end = ''):
    """
    Retrieve all Collection entries in a given time frame.
    :param db: The database object.
    :param sessionID: Current user's session ID.
    :param start: (Optional) The start of the time frame.
    :param end: (Optional) The end of the time frame.
    :return: A list of entries in a given time frame.
    """

    track_collection = db['track_collection_' + sessionID]

    result = []

    if start == '':
        start = 0.0
    if end == '':
        end = time.time()

    query = track_collection.find({
        "$and":[
            {"timestamp" : {"$gt": start}},
            {"timestamp" : {"$lt": end}}
        ]
    })

    for entry in query:
        result.append(entry)

    return result

