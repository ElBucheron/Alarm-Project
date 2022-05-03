import board
import neopixel

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

def hex_to_rgb(value):
    global MODE_BRIGHT

    value = value.lstrip('#')
    lv = len(value)

    rgb_values = tuple(int(int(value[i:i+lv//3], 16)/2) for i in range(0, lv, lv//3))

    return rgb_values

if(__name__ == '__main__'):
    pixels.fill(hex_to_rgb(default[1]))
    pixels.show()
