import board
import displayio
import framebufferio
import rgbmatrix
import time
import os

import init_matrix

LOG_FILE = 'log.txt'
filename = 'album64x64.bmp'

def display():
    # Release any existing displays
    displayio.release_displays()

    # Initialize the RGB matrix
    matrix = rgbmatrix.RGBMatrix(
    width=64, height=64, bit_depth=3,
    rgb_pins=[board.R0, board.G0, board.B0, board.R1, board.G1, board.B1],
    addr_pins=[board.ROW_A, board.ROW_B, board.ROW_C, board.ROW_D, board.ROW_E],
    clock_pin=board.CLK, latch_pin=board.LAT, output_enable_pin=board.OE)
    display = framebufferio.FramebufferDisplay(matrix)

    # Load the BMP image
    bitmap = displayio.OnDiskBitmap(filename)
    pixel_shader = bitmap.pixel_shader

    # Create a color converter to modify colors if necessary
    # You can define specific color adjustments here
    #pixel_shader = displayio.ColorConverter()  # Simple color converter

    # Create a TileGrid to fill the screen with the image
    tile_grid = displayio.TileGrid(bitmap, pixel_shader=pixel_shader,
                                x=0, y=0)

    # Create a Group to hold the TileGrid
    group = displayio.Group()
    group.append(tile_grid)

    # Set the root group to the display
    display.root_group = group

# Main loop
display()

try:
    with open(LOG_FILE) as f:
        current = f.readline()
except e:
    current = ""

# initialise start time for turning off display
now = time.time()
print(now)

while True:
    print(current)
    
    # check log file for new art
    with open(LOG_FILE) as f:
        lines = f.readlines()
        last_uploaded = lines[-1] if lines else None
        
        # if new art, detect display
        if last_uploaded != current:
            display()
            current = last_uploaded
            now = time.time()
            print(now)
    print(time.time() - now)

    # if x time has passed without new art, turn off display
    if (time.time() - now) >= 600:
        displayio.release_displays()
    
    time.sleep(1)
    pass

