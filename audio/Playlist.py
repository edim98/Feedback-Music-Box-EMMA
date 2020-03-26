# First install python-vlc using pip install python-vlc and pymongo using pip install pymongo

"""
Module which handles the media list player.
"""

import ntpath
from audio import Tracklist
from app import descriptors
from app import aggdata
from app import track_history
import os
import vlc
from app import track_history
import time
import random

media_list_player, playlist, db, sessionID = None, None, None, None
repeatFlag = False

def song_player(param_db, param_sessionID, repeat):
    """
    Instantiate the media list player and its playlist.
    Playlist is created with one random song in it.
    :param param_db: The database object.
    :param param_sessionID: Current user's session ID.
    """

    global media_list_player, playlist, db, sessionID, repeatFlag

    db = param_db
    sessionID = param_sessionID
    repeatFlag = repeat

    playlist = vlc.MediaList()

    # Add a random song to the playlist.
    allSongs = [song['name'] for song in list(Tracklist.get_all_songs(db, sessionID))]
    random_song = random.choice(allSongs)
    path = os.path.relpath('./audio/tracks/' + random_song + '.mp3')
    playlist.add_media(path)

    # Link playlist to media list player.
    media_list_player = vlc.MediaListPlayer()
    media_list_player.set_playback_mode(vlc.PlaybackMode.loop)
    media_list_player.set_media_list(playlist)

    # Add events for changing tracks.
    add_events()

def is_playing():
    """
    Check if media list player is playing at the moment.
    :return: True, if the media list player is playing. False, otherwise.
    """

    global media_list_player

    return media_list_player.is_playing()

def choose_next_song():
    """
    Choose next song to be played.
    Done by computing the scores of all available songs and then choosing the song with the highest score.
    Add the chosen song to the playlist.
    :return: Nothing.
    """

    global playlist, db, sessionID, repeatFlag

    queue = []
    all_songs = Tracklist.get_all_songs(db, sessionID)
    played_songs = [entry['trackID'] for entry in track_history.get_track_log(db, sessionID)]

    for song in all_songs:
        if song['name'] not in played_songs or repeatFlag:
            score = descriptors.get_song_score(song['descriptors'])
            queue.append((song['name'], score))

    if len(queue) == 0:
        print('Queue is empty!')
    queue.sort(key = lambda x: -x[1])

    print(queue)

    add_to_playlist(queue[0][0])


def media_changed_call_back(event):
    """
    Callback function triggered when a track is changed.
    Possible reasons: song was skipped by user, song was skipped due to a low score, system error.
    :param event: Event which triggered this callback function.
    :return: Nothing.
    """

    global db, sessionID

    # print('cb: ', event.type, event.u)
    name = get_current_song()
    song_descriptors = Tracklist.get_song(db, sessionID, name)['descriptors']

    print('Now playing: ', name)
    print('Described as: ', song_descriptors)
    print('Song score: ', descriptors.get_song_score(song_descriptors))

    # Update the Track History Collection.
    track_history.update_track_log(db, sessionID, name)


def add_events():
    """
    Set events for the media player.
    :return: Nothing.
    """

    global media_list_player

    media_player = vlc.libvlc_media_list_player_get_media_player(media_list_player)

    # Add an event for changing tracks.
    media_player.event_manager().event_attach(vlc.EventType.MediaPlayerMediaChanged, media_changed_call_back)


def play():
    """
    Play the current song in the playlist.
    :return: Nothing.
    """

    global media_list_player

    media_list_player.play()

def pause():
    """
    Pause the current song.
    :return: Nothing.
    """

    global media_list_player

    media_list_player.pause()

def add_to_playlist(name):
    """
    Add a song in the playlist.
    :param name: The name of the song.
    :return: Nothing.
    """

    global playlist

    path = os.path.relpath('./audio/tracks/' + name + '.mp3')
    playlist.add_media(path)

def get_current_song():
    """
    Get the name of the song being currently played.
    :return: The name of the song currently played.
    """

    global media_list_player

    name = media_list_player.get_media_player().get_media().get_mrl().split('/')[-1][:-4]
    name = name.replace("%20", " ")
    return name


def skip_song():
    """
    Skip the current song.
    :return: Nothing.
    """

    global media_list_player, playlist

    current_song = get_current_song()
    current_descriptors = Tracklist.get_song(db, sessionID, current_song)['descriptors']
    song_score = descriptors.get_song_score(current_descriptors)

    # Update the Aggregate Data Collection.
    aggdata.update_agg_log(db, sessionID, current_song, end_status='skip', song_score=song_score)

    choose_next_song()

    media_list_player.next()

def remove_song(name):
    """
    Remove a song from the playlist.
    :param name: The name of the song.
    :return: Nothing.
    """

    global playlist, db, sessionID

    Tracklist.remove_song(db, sessionID, name)
    name = name.replace(" ", "%20")
    index = -1
    for song in playlist:
        if name in song.get_mrl():
            index = playlist.index_of_item(song)
            break
    playlist.lock()
    playlist.remove_index(index)
    playlist.unlock()


