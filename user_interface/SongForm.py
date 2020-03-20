from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QLineEdit,
                             QFormLayout, QFileDialog, QErrorMessage,
                             QComboBox)
from PyQt5.QtGui import QIcon


class SongForm(QWidget):
    def __init__(self, main_window):
        super(SongForm, self).__init__()
        # Define parent and file selection dialog box
        self.parent = main_window
        self.file_selection = QFileDialog

        # Buttons
        self.second_button = QPushButton('Add Song')
        self.second_button.clicked.connect(self.add_song)
        self.choose_file_button = QPushButton('Choose Song')
        self.choose_file_button.clicked.connect(self.get_song_name)

        # Form entries
        self.parent.second_layout = QFormLayout()
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
        self.parent.second_layout.addRow('Song Name', self.song_name)
        self.parent.second_layout.addRow('Song Artist', self.song_artist)
        self.parent.second_layout.addRow('Genre', self.genre)
        self.parent.second_layout.addRow('Dynamics', self.dynamics)
        self.parent.second_layout.addRow('Tempo', self.tempo)
        self.parent.second_layout.addRow('Key', self.key)
        self.parent.second_layout.addRow('Lyrics', self.lyrics)
        self.parent.second_layout.addRow('Language', self.language)

        # Buttons for form
        self.parent.second_layout.addRow(self.second_button, self.choose_file_button)
        self.setLayout(self.parent.second_layout)

    # Returns name of song from MRL
    def get_song_name(self):
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

            # Add widget buttons
            label = QLabel(song_entry)
            remove_button = QPushButton()
            remove_button.setIcon(QIcon('icon.png'))
            remove_button.clicked.connect(lambda x: self.parent.remove_entry(remove_button, label))
            play = QPushButton()
            play.setIcon(QIcon('play_button.jpg'))
            play.clicked.connect(self.parent.play_song)

            # Add descriptors
            info = 'Genre: {0}, Dynamics: {1}, Tempo: {2}, Key: {3}, Lyrics: {4}, Language: {5}'.format(
                self.genre.currentText(), self.dynamics.currentText(), self.tempo.currentText(), self.key.currentText(),
                self.lyrics.currentText(), self.language.currentText())
            list_layout = self.parent.add_info_to_entry(info, label)

            # Add to layout
            self.parent.scroll_layout.addLayout(list_layout, self.parent.row, self.parent.column)
            self.parent.scroll_layout.addWidget(remove_button, self.parent.row, self.parent.column + 3)
            self.parent.scroll_layout.addWidget(play, self.parent.row, self.parent.column + 6)
            self.parent.row += 1
            self.song_name.clear()
            self.song_artist.clear()
            self.close()
        else:
            # Error in case there is no name for the song
            error_dialog = QErrorMessage()
            error_dialog.showMessage('Song name needed!')
            error_dialog.exec_()

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
