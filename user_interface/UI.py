import sys
import vlc

from PyQt5.QtWidgets import (QWidget, QLabel, QScrollArea, QPushButton,
                             QApplication, QGridLayout)
from PyQt5.QtGui import QIcon
from pymongo import MongoClient
from user_interface.SongForm import SongForm


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.row = 1
        self.column = 1

        # Main Window
        self.layout = QGridLayout()
        self.button = QPushButton('Add Song')
        self.button.clicked.connect(self.add_new_song)
        self.setLayout(self.layout)

        # Add elements to main widget
        self.scroll = QScrollArea()
        self.layout.addWidget(self.scroll)
        self.layout.addWidget(self.button)
        self.scroll.setWidgetResizable(True)

        # Define scroll area - where songs are shown
        self.scroll_content = QWidget(self.scroll)
        self.scroll_layout = QGridLayout(self.scroll_content)
        self.scroll.setWidget(self.scroll_content)
        self.dialog = SongForm(self)

        # Add existing songs from the database
        # Playlist part can be deleted
        self.playlist = vlc.MediaList()
        client = MongoClient()
        db = client['Playlists']
        playlist = db.songs
        songs = playlist.find()
        for song in songs:
            self.add_entry(song)
            self.playlist.add_media(song['title'] + '.mp3')
        self.media_player = vlc.MediaListPlayer()
        self.media_player.set_playback_mode(vlc.PlaybackMode.loop)
        self.media_player.set_media_list(self.playlist)

    # Opens the add song form
    def add_new_song(self):
        self.dialog.show()

    # Add song to playlist
    def add_entry(self, song):
        # Base elements for song entry
        label = QLabel(song['title'])
        remove_button = QPushButton()
        remove_button.setIcon(QIcon('icon.png'))
        remove_button.clicked.connect(lambda x: self.remove_entry(remove_button, label, play_button))
        play_button = QPushButton()
        play_button.setIcon(QIcon('play_button.jpg'))

        data = 'This should be changed in the final product'

        # Info panel
        list_layout = self.add_info_to_entry(data, label)

        # Add elements to scrollable layout and increment number of rows
        self.scroll_layout.addLayout(list_layout, self.row, self.column)
        self.scroll_layout.addWidget(remove_button, self.row, self.column + 3)
        self.scroll_layout.addWidget(play_button, self.row, self.column + 6)
        play_button.clicked.connect(lambda x: self.play_song(list_layout))
        self.row += 1

    # Adds the song descriptors to the entry in playlist
    def add_info_to_entry(self, data, song_name):
        list_layout = QGridLayout()
        data_label = QLabel(data)
        expand_button = QPushButton('Show info')
        expand_button.clicked.connect(lambda x: self.show_info(data_label, expand_button))
        list_layout.addWidget(song_name, 1, 1)
        list_layout.addWidget(expand_button, 1, 4)
        list_layout.addWidget(data_label, 2, 1)
        data_label.hide()
        return list_layout

    # Show the descriptors of song
    @staticmethod
    def show_info(info, button):
        if info.isHidden():
            info.show()
            button.setText('Hide info')
        else:
            info.hide()
            button.setText('Show info')

    # Removes song from playlist
    def remove_entry(self, remove_button, label, play_button):
        self.scroll_layout.removeWidget(remove_button)
        self.scroll_layout.removeWidget(label)
        self.scroll_layout.removeWidget(play_button)
        remove_button.deleteLater()
        label.deleteLater()
        play_button.deleteLater()

    # Plays the song
    def play_song(self, song_entry):
        song_index = int(self.scroll_layout.indexOf(song_entry) / 3)
        print(song_index)
        self.media_player.play_item_at_index(song_index)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
