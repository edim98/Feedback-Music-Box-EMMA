import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import os
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
# from user_interface.GUI import play_pause, skip
import user_interface.GUI.play_pause as play_pause
import user_interface.GUI.skip as skip

spi, cs, mcp, chan0 = None, None, None, None

# Stop the system/music
def play_button(channel):
    # print("Stop Button was pushed!")
    play_pause()

# Skip the current song
def skip_button(channel):
    # print("Skip Button was pushed!")
    # set_volume(check_volume())
    skip()

# Remap a value from one range to another
def remap_range(value, left_min, left_max, right_min, right_max):
    # this remaps a value from original (left) range to new (right) range
    # Figure out how 'wide' each range is
    left_span = left_max - left_min
    right_span = right_max - right_min
 
    # Convert the left range into a 0-1 range (int)
    valueScaled = int(value - left_min) / int(left_span)
 
    # Convert the 0-1 range into a value in the right range.
    return int(right_min + (valueScaled * right_span))

# Check the current desired volume, as read from the potentiometer
def check_volume():
    global chan0
    # convert 16bit adc0 (0-65535) trim pot read into 0-100 volume level
    trim_pot = chan0.value
    set_volume = remap_range(trim_pot, 0, 65535, 0, 100)
    print('Volume = {volume}%' .format(volume = set_volume))
    return set_volume

# Set the system volume to the given value
def set_volume(vol):
    set_vol_cmd = 'sudo amixer cset numid=1 -- {volume}% > /dev/null' \
    .format(volume = vol)
    os.system(set_vol_cmd)

def volume_button(channel):
    check_volume()

def buttons_initialize():

    global spi, cs, mcp, chan0

    # print(GPIO.getmode())
    GPIO.setwarnings(False) # Ignore warning for now
    #GPIO.setmode(GPIO.BOARD) # Use physical pin numbering

    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
    GPIO.add_event_detect(23,GPIO.RISING,callback=play_button) # Setup event on pin 10 rising edge

    GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
    GPIO.add_event_detect(24,GPIO.RISING,callback=skip_button) # Setup event on pin 10 rising edge


    # Add event listener for volume knob.
    # GPIO.setup(9, GPIO.IN)
    # GPIO.add_event_detect(9, GPIO.RISING, callback=volume_button)
    # GPIO.add_event_detect(9, GPIO.FALLING, callback=volume_button)

    # create the spi bus
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

    # create the cs (chip select)
    cs = digitalio.DigitalInOut(board.D22)

    # create the mcp object
    mcp = MCP.MCP3008(spi, cs)

    # create an analog input channel on pin 0
    chan0 = AnalogIn(mcp, MCP.P0)

def exit_button():
    GPIO.cleanup() # Clean up
