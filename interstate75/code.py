import board
import displayio
import framebufferio
import rgbmatrix
import time
import os

LOG_FILENAME = 'log.txt'
OUTPUT_IMAGE = 'art.bmp'
UPDATE_INTERVAL_S = 5
DISPLAY_TIMEOUT_S = 600

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
    bitmap = displayio.OnDiskBitmap(OUTPUT_IMAGE)
    pixel_shader = bitmap.pixel_shader

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
    with open(LOG_FILENAME) as f:
        current = f.readline()
except Exception as e:
    print('exception reading log file')
    current = ''

# initialise start time for turning off display
now = time.time()
#print(now)

current = ''

while True:
    
    time.sleep(UPDATE_INTERVAL_S)
        
    # check log file for new art
    try:
        with open(LOG_FILENAME, 'r') as f:
            lines = f.readlines()
            last_uploaded = lines[-1] if lines else None
            print(last_uploaded)
    except Exception as e:
        print('log file not found')
        continue

    # if new art, detect display
    if last_uploaded != current:
        display()
        current = last_uploaded
        now = time.time()
        print(now)
    print(time.time() - now)

    # if x time has passed without new art, turn off display
    if (time.time() - now) >= DISPLAY_TIMEOUT_S:
        displayio.release_displays()
    
