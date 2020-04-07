'''
Helper module for downloading songs and converting them into playable format.
'''

import os

import ffmpeg
from pytube import YouTube


def download_file(filename, link):
    '''
    Download a song and convert it to mp3.
    :param filename: The name of the song.
    :param link: The Youtube link of the song.
    '''
    yt = YouTube(link)

    # Only download if file is not found on storage.
    if not os.path.isfile('./mp4_tracks/' + filename + '.mp4'):
        yt.streams.filter(only_audio=True)[0].download(output_path='./mp4_tracks/', filename=filename)

    # Convert video file to audio file.
    if not os.path.isfile('../audio/tracks/' + filename + '.mp3'):
        ffmpeg.input('./mp4_tracks/' + filename + '.mp4').output('../audio/tracks/' + filename + '.mp3').run()
