# UAS Pilot Data Collection Tool
# CSCE 483 - Texas A&M University
# Spring 2020
# Rahul Rana, Aranpreet Gill, Maria Tyas, Juan Minor, Adolfo Herrera
# This code was created for our senior design project intended for UAS Pilot Researchers

# This file simply changes the LED color depending on the arguments provided

# Imports
import board
import neopixel
import time
import argparse

# Parse the input to get the r, g, and b values to turn the LED to
parser = argparse.ArgumentParser()
parser.add_argument('-r') #red
parser.add_argument('-g') #green
parser.add_argument('-b') #blue
args = parser.parse_args()

redVal = int(args.r)
greVal = int(args.g)
bluVal = int(args.b)

# Connect to the LED on GPIO Pin 18
pixels = neopixel.NeoPixel(board.D18, 1)

# Change the color to the one specified
try:
    pixels[0] = (redVal, greVal, bluVal)
except KeyboardInterrupt:
    pixels[0] = (0,0,0)