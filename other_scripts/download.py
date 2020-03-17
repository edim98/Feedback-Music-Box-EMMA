from pytube import YouTube
import ffmpeg
import os

def download_file(filename, link):
    yt = YouTube(link)
    if not os.path.isfile('./mp4_tracks/' + filename + '.mp4'):
        yt.streams.filter(only_audio=True)[0].download(output_path='./mp4_tracks/', filename=filename)

    ffmpeg.input('./mp4_tracks/' + filename + '.mp4').output('../audio/tracks/' + filename + '.mp3').run()


