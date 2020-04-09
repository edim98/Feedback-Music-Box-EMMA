# E.M.M.A.

## Installation instructions

* Clone repository

`sudo apt install git --upgrade`

`git clone https://git.snt.utwente.nl/design-project-feedback-music-box/e.m.m.a..git`

* Update and upgrade packages

`sudo apt update`

`sudo apt upgrade`

`sudo pip3 install --upgrade pip`

* Install opencv

First, install the required compiler:

`sudo apt install build-essential`

Install required dependencies:

`sudo apt install cmake libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev`

`sudo apt install python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev`

`sudo apt install libatlas3-base libqtgui4 libqt4-test`

Finally, install opencv for python:

`sudo apt install opencv*`

`sudo apt install python3-opencv`

`sudo pip3 install opencv-python`

Some Rasperry Pi systems report a linking error to the atomic libray.

This can be fixed using the following workaround:

Open the terminal and execute:

`echo "export LD_PRELOAD=/usr/lib/arm-linux-gnueabihf/libatomic.so.1" >> ~/.bashrc`

Followed by:

`source ~/.bashrc`

* Install matplotlib

`sudo pip3 install matplotlib`

* Install vlc

`sudo pip3 install python-vlc`

* Install mongodb

`sudo apt install mongodb`

`sudo systemctl enable mongodb`

`sudo systemctl start mongodb`

Install the python packages for 32-bit systems:

`sudo pip3 install pymongo==3.4.0`

* Install PyQt5

`sudo apt install python3-pyqt5`

* Install Microsoft Azure Cognitive Services

`sudo pip3 install --upgrade azure-cognitiveservices-vision-face`
