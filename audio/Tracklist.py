def create_playlist(db, sessionID):
    collection_name = 'songs_' + sessionID
    playlist = db[collection_name]
    return playlist

def add_song(db, sessionID, name, struct_descriptors):
    playlist = db['songs_' + sessionID]

    try:
        playlist.insert_one({
            'name': name,
            'descriptors': struct_descriptors
        })
    except:
        print('Unable to update collection: songs!')

def remove_song(db, sessionID, name):
    playlist = db['songs_' + sessionID]

    try:
        playlist.delete_one({
            'name': name
        })
    except:
        print('Unable to delete from collection: songs!')

def get_song(db, sessionID, name):
    playlist = db['songs_' + sessionID]

    try:
        result = playlist.find_one({
            'name': name
        })
    except:
        print('Unable to query collection: songs!')

    return result

def get_all_songs(db, sessionID):
    playlist = db['songs_' + sessionID]

    try:
        result = playlist.find({

        })
    except:
        print('Unable to query collection: songs!')

    return result


