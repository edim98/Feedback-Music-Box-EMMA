from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QLineEdit,
                             QFormLayout, QFileDialog, QErrorMessage,
                             QComboBox)

import user_interface.GUI_playlist as GUI_playlist
import audio.Tracklist as Tracklist


class SongForm(QWidget):
    def __init__(self, main_window):
        super(SongForm, self).__init__()
        self.setWindowTitle("Add a song")
        self.setMinimumWidth(300)
        # Define parent and file selection dialog box
        self.file_selection = QFileDialog

        # Database connection
        self.session_id = 'test'
        self.db = GUI_playlist.db

        # Buttons
        self.second_button = QPushButton('Add Song')
        self.second_button.clicked.connect(self.add_song)
        self.choose_file_button = QPushButton('Choose Song')
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
        self.lyrics.addItem('yes')
        self.lyrics.addItem('no')

        # Language
        self.language = QComboBox()
        self.add_language()

        # Add Rows to Form
        self.second_layout.addRow('Song Name', self.song_name)
        self.second_layout.addRow('Song Artist', self.song_artist)
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
        # TODO: Make this add the mp3 to our media player (maybe even to the tracks folder) and have it properly \
        #  separate artist and song name and combine it into "artist - song"
        name = self.file_selection.getOpenFileName()
        song = name[0].split('/')
        song = song[len(song) - 1].replace('.mp3', '')
        self.song_name.setText(song)

    # Adds the song from the form - should be used to also add to the database
    def add_song(self):
        # Check for song name
        if self.song_name.text() != '':
            # Check for artist
            if self.song_artist.text() != '':
                song_entry = self.song_name.text() + " - " + self.song_artist.text()
            else:
                song_entry = self.song_name.text()

            # Get descriptors
            descriptors_dict = {
                'genre': self.genre.currentText(),
                'dynamics': self.dynamics.currentText(),
                'tempo': self.tempo.currentText(),
                'key': self.key.currentText(),
                'lyrics': self.lyrics.currentText(),
                'language': self.language.currentText()
            }

            # Add the song to the database and to the GUI
            self.add_song_to_db(song_entry, descriptors_dict)
            playlist = self.db['songs_' + self.session_id]
            song = playlist.find_one({"name": song_entry})
            GUI_playlist.add_entry(song)

            self.song_name.clear()
            self.song_artist.clear()
            self.close()
        else:
            # Error in case there is no name for the song
            error_dialog = QErrorMessage()
            error_dialog.showMessage('Song name needed!')
            error_dialog.exec_()

    # Adds a song to the database
    def add_song_to_db(self, name, descriptors):
        Tracklist.add_song(self.db, self.session_id, name, descriptors)

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
