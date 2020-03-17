import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QSlider, QLabel
from PyQt5 import uic
from PyQt5.QtGui import QPixmap

import audio.Playlist2 as Playlist2

# pip3 install pyqt5 for Windows
# https://sourceforge.net/projects/winpython/files/WinPython_3.7/3.7.6.0/Winpython64-3.7.6.0.exe/download for Windows

# class Ui(QMainWindow):
#     def __init__(self):
#         super(Ui, self).__init__() # Call the inherited classes __init__ method
#         uic.loadUi('EMMA.ui', self) # Load the .ui file
#         # self.show() # Show the GUI
#         self.dead = False
#
#         self.play_pause_btn = self.findChild(QPushButton, 'play_pause_btn')
#
#     def refresh(self):
#         print("refreshed")
#         self.show()

CAMERA_IMG_PATH = "frame.png"  # Might require os.path.join(sys.path[0], "emotions_plot.png")
LIVE_IMG_PATH = "emotions_plot.png"
PROG_IMG_PATH = "progress_plot.png"


app, window, dead, frozen,play_pause_btn, skip_btn, vol_slider, vol_text, pause_EMMA_btn, registe_user_btn,camera_img, live_img, prog_img=None, None, None, None, None, None, None, None, None, None, None, None, None

class EmmaWindow(QMainWindow):
    def __init__(self):
        super(EmmaWindow, self).__init__()

    def closeEvent(self, event):
        global dead
        dead = True
        print("Closing the GUI by X")
        QMainWindow.closeEvent(self, event)
        
        
    # Maybe a refresh signal with QThread


def play_pause():
    print("play/pause")
    if play_pause_btn.text() == "Play":
        play_pause_btn.setText("Pause")
        Playlist2.play()
    else:
        play_pause_btn.setText("Play")
        Playlist2.pause()


def skip():
    print("skip")
    Playlist2.skip_song()


def change_volume():
    vol_text.setText("{}%".format(vol_slider.value()))

def start_pause_EMMA():
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
    print("TODO REGISTER USER // CALIBRATION")


def refresh():

    #  The later two parameters of scaled() are for keeping the aspect ratio and smoothing the result of scaling
    camera_img.setPixmap(QPixmap(CAMERA_IMG_PATH).scaled(camera_img.width(), camera_img.height(), 1, 1))
    live_img.setPixmap(QPixmap(LIVE_IMG_PATH).scaled(live_img.width(), live_img.height(), 1, 1))
    prog_img.setPixmap(QPixmap(PROG_IMG_PATH).scaled(prog_img.width(), prog_img.height(), 1, 1))
    

    window.show()
    #window.update()

def init():
    global app, window, dead, frozen,play_pause_btn, skip_btn, vol_slider, vol_text, pause_EMMA_btn, registe_user_btn,camera_img, live_img, prog_img
    app = QApplication(sys.argv)
    window = EmmaWindow()
    uic.loadUi('/home/eduardc/Facultate/designprojectpersonal/catalin/EMMA.ui', window)
    dead = False
    frozen = False

    play_pause_btn = window.findChild(QPushButton, 'play_pause_btn')
    play_pause_btn.clicked.connect(play_pause)

    skip_btn = window.findChild(QPushButton, 'skip_btn')
    skip_btn.clicked.connect(skip)

    vol_slider = window.findChild(QSlider, 'vol_slider')
    vol_slider.valueChanged.connect(change_volume)

    vol_text = window.findChild(QLabel, 'vol_slider_text')


    pause_EMMA_btn = window.findChild(QPushButton, 'pause_EMMA_btn')
    pause_EMMA_btn.clicked.connect(start_pause_EMMA)

    register_user_btn = window.findChild(QPushButton, 'register_user_btn')
    register_user_btn.clicked.connect(register_user)

    camera_img = window.findChild(QLabel, 'camera_img')
    live_img = window.findChild(QLabel, 'live_img')
    prog_img = window.findChild(QLabel, 'prog_img')
    
    window.show()


def run():
    init()
    app.exec_()



# window = Ui()
# window.show()
# layout = QVBoxLayout()
# layout.addWidget(QPushButton('Top'))
# layout.addWidget(QPushButton('Bottom'))
# window.setLayout(layout)
# uic.loadUi('EMMA.ui')
# window.show()
