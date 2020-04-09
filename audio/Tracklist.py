"""
Module for accessing the contents of the Song Collection.
"""

def create_song_collection(db):
    """
    Instantiate the Song Collection.
    :param db: The database object.
    :return: The Song Collection object.
    """

    collection_name = 'tracks'
    song_collection = db[collection_name]
    return song_collection

def add_song(db, name, struct_descriptors):
    """
    Add a new song in the Song Collection.
    :param db: The database object.
    :param name: The name of the song.
    :param struct_descriptors: The unique descriptors associated with this song.
    :return: Nothing.
    """

    song_collection = db['tracks']
    try:
        song_collection.insert_one({
            'name': name,
            'descriptors': struct_descriptors
        })
    except:
        print('Unable to update collection: songs!')

def remove_song(db, name):
    """
    Remove a song from the Song Collection.
    :param db: The database object.
    :param name: The name of the song.
    :return: Nothing.
    """

    song_collection = db['tracks']

    try:
        song_collection.delete_one({
            'name': name
        })
    except:
        print('Unable to delete from collection: songs!')

def get_song(db, name):
    """
    Query the Collection for a given song.
    :param db: The database object.
    :param name: The name of the song.
    :return: Collection entry matching the query.
    """

    song_collection = db['tracks']

    try:
        result = song_collection.find_one({
            'name': name
        })
    except:
        print('Unable to query collection: songs!')

    return result

def get_all_songs(db):
    """
    Retrieve all songs' information from the Songs Collection.
    :param db: The database object.
    """

    song_collection = db['tracks']

    try:
        result = song_collection.find({

        })
    except:
        print('Unable to query collection: songs!')

    return result


