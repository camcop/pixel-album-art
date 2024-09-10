import time
import board
import displayio
import framebufferio
import rgbmatrix

LOG_FILENAME = 'log.txt'
OUTPUT_IMAGE = 'art.bmp'
UPDATE_INTERVAL_S = 5
DISPLAY_TIMEOUT_S = 600

def update_display():
    """
    This function frees up the display resources before updating 
    the display with new content from the image file.
    """
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

    # Set the root group to the update_display
    display.root_group = group

# Main loop
update_display()

try:
    with open(LOG_FILENAME, 'r', encoding='utf-8') as f:
        current = f.readline()
except (FileNotFoundError, OSError) as e:
    print('Exception reading log file:', str(e))
    current = ''

# initialise start time for turning off update_display
now = time.time()
#print(now)

current = ''

while True:

    time.sleep(UPDATE_INTERVAL_S)

    # check log file for new art
    try:
        with open(LOG_FILENAME, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            last_uploaded = lines[-1] if lines else None
            print(last_uploaded)
    except (FileNotFoundError, OSError) as e:
        print('Error reading log file:', str(e))
        continue

    # if new art, detect update_display
    if last_uploaded != current:
        update_display()
        current = last_uploaded
        now = time.time()
        print(now)
    print(time.time() - now)

    # if x time has passed without new art, turn off update_display
    if (time.time() - now) >= DISPLAY_TIMEOUT_S:
        displayio.release_displays()
