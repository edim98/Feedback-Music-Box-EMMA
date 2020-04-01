import RPi.GPIO as GPIO
import os
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

def stop(channel):
    """ Called when the stop button is pressed.
        Stops the system/music/pi(?)"""
    print("Stop button was pushed!")
    # TODO: stop whatever needs stopping

def skip(channel):
    """ Called when the skip button is pressed.
        Skips the current song."""
    print("Skip button was pushed!")
    # TODO: skip current song

# Remap a value from one range to another
def remap_range(value, left_min, left_max, right_min, right_max):
    """ Remaps a value from one range to another.
       Used to convert raw ADC value to percentage."""
    left_span = left_max - left_min
    right_span = right_max - right_min
 
    valueScaled = int(value - left_min) / int(left_span)

    return int(right_min + (valueScaled * right_span))

def check_volume():
    """ Reads the ADC to determine the volume the user has requested using the potentiometer.
        Returns a percentage (0-100)"""
    vol = remap_range(trim_pot, 0, 65535, 0, 100)
    print('Requested Volume = {volume}%' .format(volume = vol))
    return vol


def set_volume(vol):
    """ Sets the audio volume of the operating system to the given value.
        expects a value between 0 and 100."""
    set_vol_cmd = 'sudo amixer cset numid=1 -- {volume}% > /dev/null' \
    .format(volume = vol)
    os.system(set_vol_cmd)

def set_up():
    """ Sets up the required pins and their response events.
        Call before any other methods in this module.
        ALWAYS CALL cleanup AFTER YOU'RE DONE!"""
    stop_pin = 8 # BCM number of the input pin connected to the stop button
    skip_pin = 10 # BCM number of the input pin connected to the skip button
    
    #GPIO.setwarnings(False) # Ignore warning for now

    GPIO.setup(stop_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set stop_pin to be an input pin and set initial value to be pulled low (off)
    GPIO.add_event_detect(stop_pin,GPIO.RISING,callback=stop) # Setup event on stop_pin rising edge

    GPIO.setup(skip_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set skip_pin to be an input pin and set initial value to be pulled low (off)
    GPIO.add_event_detect(skip_pin,GPIO.RISING,callback=skip) # Setup event on skip_pin rising edge

    # create the spi bus
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
     
    # create the cs (chip select)
    cs = digitalio.DigitalInOut(board.D22)
     
    # create the mcp object
    mcp = MCP.MCP3008(spi, cs)
     
    # create an analog input channel on pin 0
    chan0 = AnalogIn(mcp, MCP.P0)

def cleanup():
    """ Performs the necessary cleanup."""
    GPIO.cleanup()