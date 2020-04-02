"""
Module that handles a session's progress.
"""

import time

def create_progress_log(db, sessionID):
    """
    Instantiate the Progress Collection.
    :param db: The database object.
    :param sessionID: Current user's session ID.
    :return: The Progress Collection object.
    """

    collection_name = 'progress_collection_' + sessionID
    progress_collection = db[collection_name]
    return progress_collection

def update_progress_log(db, sessionID, emotion_list):
    """
    Add new entries in the Progress Collection.
    :param db: The database object.
    :param sessionID: Current user's session ID.
    :param emotion_list: A list of user emotions retrieved from the model at a given time.
    :return: Nothing.
    """

    progress_collection = db['progress_collection_' + sessionID]

    try:
        progress_collection.insert_one({
            "timestamp" : time.time(),
            "anger" : emotion_list['anger'],
            "contempt" : emotion_list['contempt'],
            "disgust" : emotion_list['disgust'],
            "fear" : emotion_list['fear'],
            "happiness" : emotion_list['happiness'],
            "neutral" : emotion_list['neutral'],
            "sadness" : emotion_list['sadness'],
            "surprise" : emotion_list['surprise']
        })
    except:
        print('Unable to update collection: progress_collection!')

def delete_track_log(db, sessionID):
    """
    Drop the Progress Collection.
    :param db: The database object.
    :param sessionID: Current user's session ID.
    :return: Nothing.
    """
    collection_name = 'progress_collection_' + sessionID
    try:
        db[collection_name].drop()
    except:
        print('Could not drop collection: progress_collection!')

def get_progress_log(db, sessionID, start = '', end = ''):
    """
    Retrieve all Collection entries in a given time frame.
    :param db: The database object.
    :param sessionID: Current user's session ID.
    :param start: (Optional) The start of the time frame.
    :param end: (Optional) The end of the time frame.
    :return: A list of entries in a given time frame.
    """

    progress_collection = db['progress_collection_' + sessionID]

    result = []

    if start == '':
        start = 0.0
    if end == '':
        end = time.time()

    query = progress_collection.find({
        "$and": [
            {'timestamp': {'$gt': start}},
            {'timestamp': {'$lt': end}}
        ]
    })

    for entry in query:
        result.append(entry)

    return result

def get_progress_trend(db, sessionID, start = '', end = ''):
    """
    Retrieve all Collection entries in a given time frame,
    in a friendly format suited for updating the Aggregate Collection.
    :param db: The database object.
    :param sessionID: Current user's session ID.
    :param start: (Optional) The start of the time frame.
    :param end: (Optional) The end of the time frame.
    """

    progress_collection = db['progress_collection_' + sessionID]

    data = get_progress_log(db, sessionID, start = start, end = end)
    result = {
        'anger': [],
        'contempt': [],
        'disgust': [],
        'fear': [],
        'happiness': [],
        'neutral': [],
        'sadness': [],
        'surprise': []
    }

    for entry in data:
        result['anger'].append(entry['anger'])
        result['contempt'].append(entry['contempt'])
        result['disgust'].append(entry['disgust'])
        result['fear'].append(entry['fear'])
        result['happiness'].append(entry['happiness'])
        result['neutral'].append(entry['neutral'])
        result['sadness'].append(entry['sadness'])
        result['surprise'].append(entry['surprise'])

    return result