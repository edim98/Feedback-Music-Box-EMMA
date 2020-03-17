'''
Module that handles a session's progress.
'''

import time

def create_progress_log(db, sessionID):
    collection_name = 'progress_collection_' + sessionID
    progress_collection = db[collection_name]
    return progress_collection

def update_progress_log(db, sessionID, emotion_list):

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
    collection_name = 'progress_collection_' + sessionID
    try:
        db[collection_name].drop()
    except:
        print('Could not drop collection: progress_collection!')

def get_progress_log(db, sessionID, start = '', end = ''):

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