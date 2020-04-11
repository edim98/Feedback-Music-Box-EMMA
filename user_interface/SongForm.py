import os

from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit,
                             QFormLayout, QFileDialog, QErrorMessage,
                             QComboBox)
from PyQt5.QtGui import QIcon

import audio.Tracklist as Tracklist
import user_interface.GUI_playlist


# from user_interface.GUI_playlist import db, add_entry

class SongForm(QWidget):
    def __init__(self, main_window):
        super(SongForm, self).__init__()
        self.setWindowTitle("Add a song")
        self.setWindowIcon(QIcon("user_interface/emma_icon.png"))
        self.setMinimumWidth(300)

        # Define file selection dialog box
        self.file_selection = QFileDialog()
        self.file_selection.setDirectory("audio/tracks")

        # Database connection
        self.session_id = 'test'
        self.db = user_interface.GUI_playlist.db

        # Buttons
        self.second_button = QPushButton('Add song')
        self.second_button.default = True
        self.second_button.clicked.connect(self.add_song)
        self.choose_file_button = QPushButton('Pick file')
        self.choose_file_button.clicked.connect(self.get_song_name)

        # Form entries
        self.second_layout = QFormLayout()
        self.song_name = QLineEdit()
        self.song_artist = QLineEdit()

        # Song Genre
        self.genre = QComboBox()
        self.add_genre()

        # Song Dynamics
        self.dynamics = QComboBox()
        self.add_dynamics()

        # Tempo
        self.tempo = QComboBox()
        self.add_tempo()

        # Key
        self.key = QComboBox()
        self.add_key()

        # Lyrics
        self.lyrics = QComboBox()
        self.lyrics.addItem('no')
        self.lyrics.addItem('yes')

        # Language
        self.language = QComboBox()
        self.add_language()

        # Error popup
        self.error_window = QErrorMessage()
        self.error_window.setWindowTitle('There was a problem...')
        self.error_window.setWindowIcon(QIcon('user_interface/emma_icon.png'))

        # Add Rows to Form
        self.second_layout.addRow('Song Artist', self.song_artist)
        self.second_layout.addRow('Song Name', self.song_name)
        self.second_layout.addRow('Genre', self.genre)
        self.second_layout.addRow('Dynamics', self.dynamics)
        self.second_layout.addRow('Tempo', self.tempo)
        self.second_layout.addRow('Key', self.key)
        self.second_layout.addRow('Lyrics', self.lyrics)
        self.second_layout.addRow('Language', self.language)

        # Buttons for form
        self.second_layout.addRow(self.second_button, self.choose_file_button)
        self.setLayout(self.second_layout)

    # Returns name of song from MRL
    def get_song_name(self):
        name = self.file_selection.getOpenFileName()
        song = name[0].split('/')
        song = song[len(song) - 1].replace('.mp3', '')
        self.song_artist.setText(song.split(' - ')[0])
        self.song_name.setText(song.split(' - ')[1])

    # Adds the song from the form - should be used to also add to the database
    def add_song(self):
        # Check for song name
        if self.song_name.text() != '':
            # Check for artist
            if self.song_artist.text() != '':
                song_entry = self.song_artist.text() + " - " + self.song_name.text()
            else:
                song_entry = self.song_name.text()

            song_in_folder = False
            for file in os.listdir("./audio/tracks"):
                if song_entry + '.mp3' == file:
                    song_in_folder = True
                    break

            if not song_in_folder:
                self.error_window.showMessage('Song file not found in audio/tracks!')
                self.error_window.exec_()
                return

            # Get descriptors
            descriptors_dict = {
                'genre': self.genre.currentText().lower(),
                'dynamics': self.dynamics.currentText().lower(),
                'tempo': self.tempo.currentText().replace(' ', ''),
                'key': self.key.currentText(),
                'lyrics': self.lyrics.currentText(),
                'language': self.language.currentText().lower()
            }

            # Add the song to the database and to the GUI
            self.add_song_to_db(song_entry, descriptors_dict)
            playlist = self.db['tracks']
            song = playlist.find_one({"name": song_entry})
            user_interface.GUI_playlist.add_entry(song)

            self.song_name.clear()
            self.song_artist.clear()
            self.close()
        else:
            self.error_window.showMessage('Song name needed!')
            self.error_window.exec_()

    # Adds a song to the database
    def add_song_to_db(self, name, descriptors):
        Tracklist.add_song(self.db, name, descriptors)

    # These are self explanatory
    def add_genre(self):
        self.genre.addItem('Rock')
        self.genre.addItem('Metal')
        self.genre.addItem('Electronic')
        self.genre.addItem('R&B')
        self.genre.addItem('Pop')
        self.genre.addItem('Folk')
        self.genre.addItem('Latin')
        self.genre.addItem('Punk')
        self.genre.addItem('Jazz')
        self.genre.addItem('Blues')
        self.genre.addItem('Classical')
        self.genre.addItem('Country')

    def add_dynamics(self):
        self.dynamics.addItem('Low')
        self.dynamics.addItem('Medium')
        self.dynamics.addItem('High')

    def add_tempo(self):
        self.tempo.addItem('< 30')
        self.tempo.addItem('40 - 60')
        self.tempo.addItem('60 - 66')
        self.tempo.addItem('66 - 76')
        self.tempo.addItem('76 - 108')
        self.tempo.addItem('108 - 120')
        self.tempo.addItem('120 - 168')
        self.tempo.addItem('200+')

    def add_key(self):
        self.key.addItem('A major')
        self.key.addItem('A minor')
        self.key.addItem('Ab major')
        self.key.addItem('Ab minor')
        self.key.addItem('B major')
        self.key.addItem('B minor')
        self.key.addItem('Bb major')
        self.key.addItem('Bb minor')
        self.key.addItem('C major')
        self.key.addItem('C minor')
        self.key.addItem('D major')
        self.key.addItem('D minor')
        self.key.addItem('Db major')
        self.key.addItem('Db minor')
        self.key.addItem('E major')
        self.key.addItem('E minor')
        self.key.addItem('Eb major')
        self.key.addItem('Eb minor')
        self.key.addItem('F major')
        self.key.addItem('F minor')
        self.key.addItem('F# major')
        self.key.addItem('F# minor')
        self.key.addItem('G major')
        self.key.addItem('G minor')

    def add_language(self):
        self.language.addItem('None')
        self.language.addItem('Romanian')
        self.language.addItem('English')
        self.language.addItem('Dutch')
        self.language.addItem('German')
        self.language.addItem('Portuguese')
        self.language.addItem('Lithuanian')
        self.language.addItem('Spanish')
        self.language.addItem('French')
        self.language.addItem('Italian')
        self.language.addItem('Other')
