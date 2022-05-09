# Simple test for NeoPixels on Raspberry Pi
import sys
import time
import board
import neopixel
import datetime as dt
import pendulum
import math
import signal
from random import randrange
from random import uniform
from cozy_fire import fire

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D12

# The number of NeoPixels
num_pixels = 64

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.1, auto_write=False,
                           pixel_order=ORDER)

pixel_off = "#000000"
COLOR_1 = "#FDE74C"
COLOR_2 = "#5BC0EB"

ZERO = [[1,1,1,1,1],[1,0,0,0,1],[1,1,1,1,1]]
UN = [[0,0,0,0,1],[1,1,1,1,1],[0,1,0,0,1]]
DEUX = [[1,1,1,0,1],[1,0,1,0,1],[1,0,1,1,1]]
TROIS = [[1,1,1,1,1],[1,0,1,0,1],[1,0,0,0,1]]
QUATRE = [[0,1,1,1,1],[0,0,1,0,0],[1,1,1,0,0]]
CINQ = [[1,0,1,1,1],[1,0,1,0,1],[1,1,1,0,1]]
SIX = [[1,0,1,1,1],[1,0,1,0,1],[1,1,1,1,1]]
SEPT = [[1,1,1,1,1],[1,0,0,0,0],[1,0,0,0,0]]
HUIT = [[1,1,1,1,1],[1,0,1,0,1],[1,1,1,1,1]]
NEUF = [[1,1,1,1,1],[1,0,1,0,1],[1,1,1,0,1]]
CHIFFRE = [ZERO,UN,DEUX,TROIS,QUATRE,CINQ,SIX,SEPT,HUIT,NEUF]

TABLEAU_HORLOGE = []


tz = pendulum.timezone('Europe/Paris')
heure = dt.datetime.now(tz).hour

def hex_to_rgb(value):

    value = value.lstrip('#')
    lv = len(value)
    rgb_values = tuple(int(value[i:i+lv//3], 16) for i in range(0, lv, lv//3))

    return rgb_values


def horloge(heure, minutes):
    global TABLEAU_HORLOGE

    "Affichage de l'heure"
    if(heure > 9):
        heure1 = heure // 10 ** int(math.log(heure, 10))
        heure2 = heure % 10
    else:
        heure1 = 0
        heure2 = heure
    if(minutes > 9):
        minute1 = minutes // 10 ** int(math.log(minutes, 10))
        minute2 = minutes % 10
    else:
        minute1 = 0
        minute2 = minutes

    #print("Heure:", afficheHeure)

    initTableauHorloge()

    x = 0
    y = 0
    for i in range(0, 3):
        for j in range(3, 8):
            pixel = CHIFFRE[minute2][x][y]
            if pixel:
                TABLEAU_HORLOGE[i][j] = COLOR_2
            y = y + 1
        x = x + 1
        y = 0

    x = 0
    for i in range(4, 7):
        for j in range(3, 8):
            pixel = CHIFFRE[minute1][x][y]
            if pixel:
                TABLEAU_HORLOGE[i][j] = COLOR_2
            y = y + 1
        x = x + 1
        y = 0

    x = 0
    for i in range(1, 4):
        for j in range(0, 5):
            pixel = CHIFFRE[heure2][x][y]
            if pixel:
                TABLEAU_HORLOGE[i][j] = COLOR_1
            y = y + 1
        x = x + 1
        y = 0

    x = 0
    for i in range(5, 8):
        for j in range(0, 5):
            pixel = CHIFFRE[heure1][x][y]
            if pixel:
                TABLEAU_HORLOGE[i][j] = COLOR_1
            y = y + 1
        x = x + 1
        y = 0


def tableauVersLEDS():
    global COULEURS
    global TABLEAU_HORLOGE

    tab = TABLEAU_HORLOGE

    i = 0
    led = 0
    while i < 7:
        for j in reversed(range(8)):
            pixels[led] = hex_to_rgb(tab[i][j])
            led = led + 1
        i = i + 1

        for j in range(8):
            pixels[led] = hex_to_rgb(tab[i][j])
            led = led + 1
        i = i + 1

    pixels.show()

def initTableauHorloge():
    global TABLEAU_HORLOGE

    TABLEAU_HORLOGE = []
    for i in range(8):
    	TABLEAU_HORLOGE.append([pixel_off,pixel_off,pixel_off,pixel_off,pixel_off,pixel_off,pixel_off,pixel_off])

def turnOffLeds():
    pixels.fill((0, 0, 0))
    pixels.show()

def terminateProcess(signalNumber, frame):
    turnOffLeds()
    exit(0)


if(__name__ == '__main__'):

    signal.signal(signal.SIGTERM, terminateProcess)

    try:
        print("[!] Press ctrl-c to exit")

        print("Reinitialisation des tableaux...")
        initTableauHorloge()

        changeHeure = int
        changeMinute = int

        heure = dt.datetime.now(tz).hour
        minutes = dt.datetime.now(tz).minute
        horloge(heure, minutes)
        tableauVersLEDS()
        
        while(heure < int(sys.argv[1])):

            heure = dt.datetime.now(tz).hour
            minutes = dt.datetime.now(tz).minute

            minutesNow = minutes % 10

            if(minutesNow != changeMinute):
                if(heure != changeHeure):
                    changeHeure = heure

                changeMinute = minutesNow
                
                horloge(heure, minutes)
                tableauVersLEDS()

            time.sleep(1)

        turnOffLeds()
        print("Fin du programme.")

    except KeyboardInterrupt:
        terminateProcess(0,0)
