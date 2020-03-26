from PyQt5.QtWidgets import (QWidget, QLabel, QScrollArea, QPushButton,
                             QApplication, QGridLayout, QSizePolicy)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize
from pymongo import MongoClient
from user_interface.SongForm import SongForm
import user_interface.GUI as GUI
import audio.Playlist2 as Playlist2

row, column, scroll_layout, scroll_contents, dialog = 0, 0, None, None, None

client = MongoClient()
db = client.test_database


def init(window):
    global row, column, scroll_layout, dialog, scroll_contents
    row = 1
    column = 1
    scroll_layout = window.findChild(QGridLayout, 'playlist_grid')
    scroll_contents = window.findChild(QWidget, 'scroll_contents')
    dialog = SongForm(window)
    add_song_btn = window.findChild(QPushButton, 'add_song_btn')
    add_song_btn.clicked.connect(add_new_song)

    playlist = db.songs_test
    songs = playlist.find()
    for song in songs:
        add_entry(song)


def add_new_song():
    dialog.show()


def add_entry(song):
    global row, column
    label = QLabel(song['name'])
    remove_button = QPushButton()
    remove_button.setIcon(QIcon('user_interface/remove_button.png'))
    remove_button.setIconSize(QSize(25, 25))
    remove_button.setStyleSheet("QPushButton {padding : 5px}")

    play_button = QPushButton()
    play_button.setIcon(QIcon('user_interface/play_button.png'))
    play_button.setIconSize(QSize(25, 25))
    play_button.setStyleSheet("QPushButton {padding : 5px}")

    data = str(song['descriptors'])

    scroll_layout.addWidget(label, row, column)
    scroll_layout.addWidget(play_button, row, column + 1)
    scroll_layout.addWidget(remove_button, row, column + 2)

    label.setToolTip(data)
    label.setToolTipDuration(5000)
    remove_button.clicked.connect(lambda x: remove_entry(remove_button, label, play_button))
    play_button.clicked.connect(lambda x: play_entry(label))

    scroll_contents.setMinimumHeight(row * 44)
    row += 1


def remove_entry(remove_button, label, play_button):
    global row
    row -= 2  # Deletes two rows to make up for extra spacing
    scroll_contents.setMinimumHeight(row * 44)
    row += 1  # Adds one more row to keep up with the real value of rows
    scroll_layout.removeWidget(remove_button)
    scroll_layout.removeWidget(label)
    scroll_layout.removeWidget(play_button)
    remove_button.deleteLater()
    label.deleteLater()
    play_button.deleteLater()


def play_entry(label):
    Playlist2.play_song(label)
    if not Playlist2.is_playing():
        GUI.play_pause_btn.setText("Pause")
        GUI.now_playing_text.show()
        GUI.current_song_text.setText("{}".format(label.text()))
        print("set text to : {}".format(label.text()))
        if not GUI.current_song_text.isVisible():
            GUI.current_song_text.show()
    else:
        GUI.play_pause_btn.setText("Play")
        Playlist2.pause()
        GUI.now_playing_text.hide()
