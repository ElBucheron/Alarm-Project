import time
import board
import neopixel
import signal

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

default = ["#000000", "#FA7921"]

TABLEAU_LED = []

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
 
    rgb_values = tuple(int(int(value[i:i+lv//3], 16)/2) for i in range(0, lv, lv//3))

    return rgb_values

def addLineLight(line):
    global TABLEAU_LED

    line = 7-line
    
    for i in range(8):
        TABLEAU_LED[i][line] = default[1]

def tableauVersLEDS():
    global TABLEAU_LED

    tab = TABLEAU_LED

    i = 0
    led = 0
    while i < 8:
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
    global TABLEAU_LED
    global default

    TABLEAU_HORLOGE = []
    for i in range(8):
    	TABLEAU_LED.append([default[0],default[0],default[0],default[0],default[0],default[0],default[0],default[0]])

def turnOffLeds():
    pixels.fill((0, 0, 0))
    pixels.show()

def terminateProcess(signalNumber, frame):
    turnOffLeds()
    exit(0)

def startSlowLight():
    global default
    global TABLEAU_LED
    signal.signal(signal.SIGTERM, terminateProcess)
    try:
        print("[+] Starting Slow Light")
        print("Reinitialisation des tableaux...")
        initTableauHorloge()

        for i in range(8):
            addLineLight(i)
            #print(TABLEAU_HORLOGE)
            tableauVersLEDS()
            time.sleep(75)

    except KeyboardInterrupt:
        terminateProcess(0,0)

if(__name__ == '__main__'):
    print("[!] Press ctrl-c to exit")
    startSlowLight()
