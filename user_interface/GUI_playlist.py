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
    """
    Initializes the playlist widget and links elements to their functions.
    :param window: The parent window.
    """
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
    """
    Pops up a form for adding a new track to the playlist.
    """
    dialog.show()


def add_entry(song):
    """
    Creates and links to functionality the required elements for a song entry and adds it to the playlist widget.
    :param song: Song object, created from a database query.
    """
    global row, column
    label = QLabel(song['name'])
    remove_button = QPushButton()
    remove_button.setIcon(QIcon('user_interface/remove_button.png'))
    remove_button.setIconSize(QSize(25, 25))
    remove_button.setStyleSheet("QPushButton {padding : 5px}")  # Set the padding of the button icon

    play_button = QPushButton()
    play_button.setIcon(QIcon('user_interface/play_button.png'))
    play_button.setIconSize(QSize(25, 25))
    play_button.setStyleSheet("QPushButton {padding : 5px}")  # Set the padding of the button icon

    data = str(song['descriptors'])

    scroll_layout.addWidget(label, row, column)
    scroll_layout.addWidget(play_button, row, column + 1)
    scroll_layout.addWidget(remove_button, row, column + 2)

    label.setToolTip(data)
    label.setToolTipDuration(5000)

    remove_button.clicked.connect(lambda x: remove_entry(label, play_button, remove_button))
    play_button.clicked.connect(lambda x: play_entry(label))

    scroll_contents.setMinimumHeight(row * 44)  # Adjusts to accommodate to the new entry.
    row += 1  # Keeps up with the current number of rows in the playlist widget.


def remove_entry(label, play_button, remove_button):
    """
    Deletes a given entry from the playlist widget and readjusts the size.
    :param label: The label containing the name of the entry.
    :param play_button: The play button of the entry.
    :param remove_button: The remove button of the entry.
    """
    global row
    row -= 2  # Deletes two rows to make up for extra spacing.
    scroll_contents.setMinimumHeight(row * 44)
    row += 1  # Adds one more row to keep up with the real value of rows.

    scroll_layout.removeWidget(remove_button)
    scroll_layout.removeWidget(label)
    scroll_layout.removeWidget(play_button)
    remove_button.deleteLater()
    label.deleteLater()
    play_button.deleteLater()


def play_entry(label):
    """
    Called to trigger the playing/pausing of a specific entry, given its label. This also sets specific buttons
    and labels to appropriate states to reflect the change.
    :param label: The label containing the name of the entry to be played or paused.
    :return:
    """
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
