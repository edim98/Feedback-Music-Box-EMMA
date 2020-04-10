import os
import sys

from cv2 import imwrite
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QSlider, QLabel, QErrorMessage

import audio.Playlist as Playlist
import user_interface.GUI_playlist as GUI_playlist
from user_interface.face_utils import get_frame
# from hardware.buttons import check_volume
from hardware.buttons import buttons_initialize, check_volume

CAMERA_IMG_PATH = "frame.png"
LIVE_IMG_PATH = "emotions_plot.png"
PROG_IMG_PATH = "progress_plot.png"

app, window, dead, frozen, play_pause_btn, skip_btn, vol_slider, vol_text, pause_EMMA_btn, registe_user_btn, camera_img, live_img, prog_img, current_song_text, now_playing_text = None, None, None, None, None, None, None, None, None, None, None, None, None, None, None
webcam, sessionID, faceverification, register_window = None, None, None, None


class EmmaWindow(QMainWindow):
    def __init__(self):
        super(EmmaWindow, self).__init__()

    def closeEvent(self, event):
        global dead
        dead = True  # Set the dead signal to True. EMMA should shut down.
        QMainWindow.closeEvent(self, event)


def setSomeVariables(vc, session, fv):
    global webcam, sessionID, faceverification
    webcam = vc
    sessionID = session
    faceverification = fv


def play_pause():
    """
    Called when the Play/Pause button is pressed. Starts/stops/resumes a song.
    """
    if not Playlist.is_playing():
        play_pause_btn.setText("Pause")
        Playlist.play()
        now_playing_text.show()
        if not current_song_text.isVisible():
            current_song_text.setText("{}".format(Playlist.get_current_song()))
            current_song_text.show()
    else:
        play_pause_btn.setText("Play")
        Playlist.pause()
        now_playing_text.hide()


def skip():
    """
    Called when the Skip button is pressed. Skips the song, according to the implementation of the media player.
    """
    Playlist.skip_song()
    current_song_text.setText("{}".format(Playlist.get_current_song()))
    play_pause_btn.setText("Pause")


def change_volume():
    """
    Called when the slider value changes. Changes the volume of the player accordingly.
    """
    vol_text.setText("{}%".format(vol_slider.value()))
    Playlist.set_volume(vol_slider.value())

def set_volume():
    current_volume = check_volume()
    vol_slider.setValue(current_volume)
    Playlist.set_volume(current_volume)

def start_pause_EMMA():
    """
    Called when the EMMA is paused or resumed. Enables/disables the media controls. Pauses the emotion tracking system.
    """
    global frozen
    if pause_EMMA_btn.text() == "Pause EMMA":
        frozen = True
        pause_EMMA_btn.setText("Resume EMMA")
    else:
        frozen = False
        pause_EMMA_btn.setText("Pause EMMA")


def register_user():
    """
    Called when a new user is to be registered for face identification. Takes a frame, stores it and tries to get
    a face id from Azure Face.
    """
    global webcam, sessionID, faceverification, register_window

    frame = get_frame(webcam)
    path = os.path.relpath('user_verification/' + sessionID)
    if not os.path.isdir(path):
        os.mkdir(path)
    imwrite(path + '/' + sessionID + '.png', frame)

    face_id = faceverification.get_target_face_id()
    if face_id:
        faceverification.set_target_face_id(face_id)
        faceverification.setStatus(True)
        register_window.showMessage('Face successfully registered!')
    else:
        register_window.showMessage('Face was not recognized by Azure. Please readjust your positioning!')
    register_window.exec_()


def refresh_frame():
    """
    Called to refresh and display only the camera feed image.
    """
    camera_img.setPixmap(QPixmap(CAMERA_IMG_PATH).scaled(camera_img.width(), camera_img.height(), 1, 1))
    camera_img.show()


def refresh():
    """
    Called when new images are to be displayed on the screen (i.e. new reaction from the user). Sets a new pixmap
    component for each of the image object on the screen. Finally, repaints the whole window.
    """

    #  The later two parameters of scaled() are for keeping the aspect ratio and smoothing the result of scaling
    camera_img.setPixmap(QPixmap(CAMERA_IMG_PATH).scaled(camera_img.width(), camera_img.height(), 1, 1))
    live_img.setPixmap(QPixmap(LIVE_IMG_PATH).scaled(live_img.width(), live_img.height(), 1, 1))
    prog_img.setPixmap(QPixmap(PROG_IMG_PATH).scaled(prog_img.width(), prog_img.height(), 1, 1))

    if Playlist.is_playing():
        current_song_text.setText("{}".format(Playlist.get_current_song()))

    window.show()


def init():
    """
    Initializes all the objects on the GUI by loading "EMMA.ui" which contains all the necessary UI elements and
    their placing. References them to properly named objects so they can be used in code. Displays the GUI.
    """
    global app, window, dead, frozen, play_pause_btn, skip_btn, vol_slider, vol_text, pause_EMMA_btn, registe_user_btn, \
        camera_img, live_img, prog_img, current_song_text, now_playing_text, register_window
    app = QApplication(sys.argv)
    window = EmmaWindow()
    uic.loadUi(os.path.join(sys.path[0], "user_interface/EMMA.ui"), window)
    dead = False  # Used to signal if EMMA and the GUI should stop.
    frozen = False  # Used to signal if EMMA should pause.

    # Find and reference the UI elements from EMMA.ui
    play_pause_btn = window.findChild(QPushButton, 'play_pause_btn')
    skip_btn = window.findChild(QPushButton, 'skip_btn')
    pause_EMMA_btn = window.findChild(QPushButton, 'pause_EMMA_btn')
    register_user_btn = window.findChild(QPushButton, 'register_user_btn')
    vol_slider = window.findChild(QSlider, 'vol_slider')
    vol_text = window.findChild(QLabel, 'vol_slider_text')
    current_song_text = window.findChild(QLabel, 'current_song_text')
    now_playing_text = window.findChild(QLabel, 'now_playing_text')
    camera_img = window.findChild(QLabel, 'camera_img')
    live_img = window.findChild(QLabel, 'live_img')
    prog_img = window.findChild(QLabel, 'prog_img')
    GUI_playlist.init(window)  # Links the playlist widget to its functions
    Playlist.set_volume(vol_slider.value())  # Make sure VLC has the same value as the slider initial value.

    register_window = QErrorMessage()
    register_window.setWindowTitle('Face Identification')
    register_window.setWindowIcon(QIcon('user_interface/emma_icon.png'))

    # Connects elements to callback functions
    play_pause_btn.clicked.connect(play_pause)
    skip_btn.clicked.connect(skip)
    vol_slider.valueChanged.connect(change_volume)
    pause_EMMA_btn.clicked.connect(start_pause_EMMA)
    register_user_btn.clicked.connect(register_user)
    current_song_text.hide()
    now_playing_text.hide()

    buttons_initialize(play_pause, skip, set_volume)

    window.show()


def run():
    """
    Initializes the GUI and runs it as an application.
    """
    init()
    app.exec_()
