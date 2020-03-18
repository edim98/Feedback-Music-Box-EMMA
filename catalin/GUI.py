import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QSlider, QLabel
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
import audio.Playlist2 as Playlist2

CAMERA_IMG_PATH = "frame.png"  # Might require os.path.join(sys.path[0], "emotions_plot.png")
LIVE_IMG_PATH = "emotions_plot.png"
PROG_IMG_PATH = "progress_plot.png"

app, window, dead, frozen, play_pause_btn, skip_btn, vol_slider, vol_text, pause_EMMA_btn, registe_user_btn, camera_img, live_img, prog_img = None, None, None, None, None, None, None, None, None, None, None, None, None


class EmmaWindow(QMainWindow):
    def __init__(self):
        super(EmmaWindow, self).__init__()

    def closeEvent(self, event):
        global dead
        dead = True  # Set the dead signal to True. EMMA should shut down.
        print("Closing the GUI by X")
        QMainWindow.closeEvent(self, event)

    # Maybe a refresh signal with QThread


def play_pause():
    """
    Called when the Play/Pause button is pressed. Starts/stops/resumes a song.
    """
    print("play/pause")
    if play_pause_btn.text() == "Play":
        play_pause_btn.setText("Pause")
        Playlist2.play()
    else:
        play_pause_btn.setText("Play")
        Playlist2.pause()


def skip():
    """
    Called when the Skip button is pressed. Skips the song, according to the implementation of the media player.
    """
    print("skip")
    Playlist2.skip_song()


def change_volume():
    """
    Called when the slider value changes. Changes the volume of the player accordingly.
    :todo: Make this actually change the volume of the player/os
    """
    vol_text.setText("{}%".format(vol_slider.value()))


def start_pause_EMMA():
    """
    Called when the EMMA is paused or resumed. Enables/disables the media controls and sets
    """
    global frozen
    if pause_EMMA_btn.text() == "Pause EMMA":
        frozen = True
        pause_EMMA_btn.setText("Resume EMMA")
        play_pause_btn.setEnabled(False)
        skip_btn.setEnabled(False)
        vol_slider.setEnabled(False)
    else:
        frozen = False
        pause_EMMA_btn.setText("Pause EMMA")
        play_pause_btn.setEnabled(True)
        skip_btn.setEnabled(True)
        vol_slider.setEnabled(True)


def register_user():
    """
    Called when a new user is to be registered for face recognition. Should prompt a new window where the
    registering/calibration process takes place.
    :todo: Make this.
    """
    print("TODO REGISTER USER // CALIBRATION")


def refresh():
    """
    Called when new images are to be displayed on the screen (i.e. new reaction from the user). Sets new pixmap
    component for each of the image object on the screen. Finally, repaints the whole window.
    """

    #  The later two parameters of scaled() are for keeping the aspect ratio and smoothing the result of scaling
    camera_img.setPixmap(QPixmap(CAMERA_IMG_PATH).scaled(camera_img.width(), camera_img.height(), 1, 1))
    live_img.setPixmap(QPixmap(LIVE_IMG_PATH).scaled(live_img.width(), live_img.height(), 1, 1))
    prog_img.setPixmap(QPixmap(PROG_IMG_PATH).scaled(prog_img.width(), prog_img.height(), 1, 1))

    window.show()


def init():
    """
    Initializes all the objects on the GUI by loading "EMMA.ui" which contains all the necessary UI elements and
    their placing. References them to properly named objects so they can be used in code. Displays the GUI.
    """
    global app, window, dead, frozen, play_pause_btn, skip_btn, vol_slider, vol_text, pause_EMMA_btn, registe_user_btn, \
        camera_img, live_img, prog_img
    app = QApplication(sys.argv)
    window = EmmaWindow()
    uic.loadUi('/home/eduardc/Facultate/designprojectpersonal/catalin/EMMA.ui', window)
    dead = False  # Used to signal if EMMA and the GUI should stop.
    frozen = False  # Used to signal if EMMA should pause.

    # Find and reference the UI elements from EMMA.ui
    play_pause_btn = window.findChild(QPushButton, 'play_pause_btn')
    skip_btn = window.findChild(QPushButton, 'skip_btn')
    pause_EMMA_btn = window.findChild(QPushButton, 'pause_EMMA_btn')
    register_user_btn = window.findChild(QPushButton, 'register_user_btn')
    vol_slider = window.findChild(QSlider, 'vol_slider')
    vol_text = window.findChild(QLabel, 'vol_slider_text')
    camera_img = window.findChild(QLabel, 'camera_img')
    live_img = window.findChild(QLabel, 'live_img')
    prog_img = window.findChild(QLabel, 'prog_img')

    # Connects elements to callback functions
    play_pause_btn.clicked.connect(play_pause)
    skip_btn.clicked.connect(skip)
    vol_slider.valueChanged.connect(change_volume)
    pause_EMMA_btn.clicked.connect(start_pause_EMMA)
    register_user_btn.clicked.connect(register_user)

    window.show()


def run():
    """
    Initializes the GUI and runs it as an application.
    """
    init()
    app.exec_()
