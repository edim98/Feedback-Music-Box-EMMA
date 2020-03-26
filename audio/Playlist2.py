# First install python-vlc using pip install python-vlc and pymongo using pip install pymongo
# To add songs use 'add song_name'. It does not need the file extension, for now
# To skip a song use 'skip'
# To remove a song use 'remove song_name'. It does not need the file extension, for now

# TODO: Change module name to something else...

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

def song_player(param_db, param_sessionID):
    global media_list_player, playlist, db, sessionID

    db = param_db
    sessionID = param_sessionID

    playlist = vlc.MediaList()

    allSongs = [song['name'] for song in list(Tracklist.get_all_songs(db, sessionID))]
    random_song = random.choice(allSongs)
        # path = os.path.relpath('./audio/tracks/' + random_song + '.mp3')
    path = os.path.relpath('./audio/tracks/' + random_song + '.mp3')
    playlist.add_media(path)
    media_list_player = vlc.MediaListPlayer()
    media_list_player.set_playback_mode(vlc.PlaybackMode.loop)
    media_list_player.set_media_list(playlist)

    add_events()

def is_playing():
    global media_list_player

    return media_list_player.is_playing()

def choose_next_song():
    global playlist, db, sessionID
    queue = []
    all_songs = Tracklist.get_all_songs(db, sessionID)
    played_songs = [entry['trackID'] for entry in track_history.get_track_log(db, sessionID)]

    for song in all_songs:
        if song['name'] not in played_songs:
            score = descriptors.get_song_score(song['descriptors'])
            queue.append((song['name'], score))

    if len(queue) == 0:
        print('Queue is empty!')
    queue.sort(key = lambda x: -x[1])

    print(queue)

    add_to_playlist(queue[0][0])



def media_changed_call_back(event):
    global db, sessionID

    current_time = time.time()
    print('cb: ', event.type, event.u)
    name = get_current_song()
    song_descriptors = Tracklist.get_song(db, sessionID, name)['descriptors']
    print('Now playing: ', name)
    print('Described as: ', song_descriptors)
    print('Song score: ', descriptors.get_song_score(song_descriptors))
    track_history.update_track_log(db, sessionID, name)

    # lastPlayed = track_history.get_track_log(db, sessionID, end = current_time)[-1]['trackID']
    # lastPlayeddescriptors = Tracklist.get_song(db, sessionID, lastPlayed)['descriptors']
    # lastPlayed_score = descriptors.get_song_score(lastPlayeddescriptors)
    # aggdata.update_agg_log(db, sessionID, lastPlayed, end_status='???', song_score=lastPlayed_score)



def add_events():
    global media_list_player
    media_player = vlc.libvlc_media_list_player_get_media_player(media_list_player)
    media_player.event_manager().event_attach(vlc.EventType.MediaPlayerMediaChanged, media_changed_call_back)


def play():
    global media_list_player
    media_list_player.play()

def pause():
    global media_list_player
    media_list_player.pause()

def add_to_playlist(name):
    global playlist
    #     path = os.path.relpath('./audio/tracks/' + name + '.mp3')
    path = os.path.relpath('./audio/tracks/' + name + '.mp3')
    playlist.add_media(path)

def get_current_song():
    global media_list_player
    name = media_list_player.get_media_player().get_media().get_mrl().split('/')[-1][:-4]
    name = name.replace("%20", " ")
    return name


def skip_song():
    global media_list_player, playlist

    current_song = get_current_song()
    current_descriptors = Tracklist.get_song(db, sessionID, current_song)['descriptors']
    song_score = descriptors.get_song_score(current_descriptors)
    aggdata.update_agg_log(db, sessionID, current_song, end_status='skip', song_score=song_score)

    choose_next_song()

    media_list_player.next()

def remove_song(name):
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


def set_volume(value):
    global media_list_player
    if media_list_player:
        vlc.libvlc_audio_set_volume(media_list_player.get_media_player(), value)


def play_song(label):
    name = label.text()
    path = os.path.relpath('./audio/tracks/' + name + '.mp3')
    playlist.add_media(path)

    media_list_player.play_item_at_index(len(playlist) - 1)
