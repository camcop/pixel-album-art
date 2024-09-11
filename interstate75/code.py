import time
import board
import displayio
import framebufferio
import rgbmatrix

OUTPUT_IMAGE = 'art.bmp'
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
    return time.time()

# Main loop
now = update_display()

while True:
    if (time.time() - now) >= DISPLAY_TIMEOUT_S:
        displayio.release_displays()
