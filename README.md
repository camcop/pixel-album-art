# README

## Overview

Dynamically display the currently playing album art on an LED matrix panel. This project integrates with Last.fm to fetch the album art and handles image format conversion, resizing, and uploading to the board.

## Key Features

- **Service Agnostic**: Compatible with any music service that scrobbles to Last.fm.
- **Public API Use**: No sign-up needed; the project utilizes a public API key provided in the code.
- **Multi-Format Support**: Handles JPEG, PNG, BMP, GIF, and ICO file types.
- **Optional Manual Image Uploading**: Easily upload your own images for display on the board.

## Hardware

- [Interstate75](https://thepihut.com/products/interstate-75)
- [RGB Full-Colour LED Matrix Panel - 2mm Pitch, 64x64 Pixels](https://thepihut.com/products/rgb-full-colour-led-matrix-panel-2mm-pitch-64x64-pixels)

## Hardware setup

1. Follow [Pimoronmi's guide](https://learn.pimoroni.com/article/getting-started-with-interstate-75#introduction) to attach the LED matrix panel to the Interstate75

2. Install [CircuitPython](https://circuitpython.org/board/pimoroni_interstate75/) on the Interstate75, following the guide from [Pimoroni](https://learn.pimoroni.com/article/getting-started-with-interstate-75#circuitpython)

## Installation

1. To set up the project, ensure you have Python installed and use the following command to install the required packages:

```bash
pip install -r requirements.txt
```

2. Copy `code.py` from the `interstate75` folder of the project to the root of the drive (which will be called CIRCUITPY). This code will run every time the board boots

3. Press `RST` button on the board to restart

## Configuration

Before running the application, create a .env file at the root of the project with the following variable:

```
LASTFM_USER=<your_lastfm_username>
```

Then configure necessary settings in config.py:

```python
BOARD_DRIVE_LETTER = 'D:'
IMAGE_DIR = 'images' # Optional
LOG_FILENAME = 'log.txt' # Optional
```

## Usage

To start the application, run the main script:

```bash
python main.py
```

### (Optional) Manual Image Upload

To manually upload an image, use the `manual_upload` function in `manual_upload.py`. Specify parameters such as:

- `filename`: path of the image file to upload
- `width`: desired width for the resized image
- `height`: desired height for the resized image
- `format`: the format that the image should be converted to (BMP is best)

### Logging

Logs of upload activities are stored in the file specified by `LOG_FILENAME`.

## Dependencies

The project relies on a few external libraries, listed in `requirements.txt`:

- `Pillow` for image processing
- `python-dotenv` for environment variable management
- `Requests` for making HTTP requests
- `Unidecode` for string manipulation


## Further Information

For additional details about the functions being used, please refer to the respective Python files in this project:

- `write_to_board.py`
- `convert.py`
- `download.py`
- `manual_upload.py`
- `config.py`

## Inspiration and resources

This project incorporate code from the [lastfm-user-data-api](https://github.com/hankhank10/lastfm-user-data-api/tree/master) project by [<NAME>](https://github.com/hankhank10).

This project was inspired by my previous project NowPlaying (which displays the currently playing track on a Waveshare e-ink display), as well as a similar project shared by [this reddit user](https://www.reddit.com/r/raspberry_pi/comments/ziz4hk/my_64x64_rgb_led_matrix_album_art_display_pi_3b/).

To understand how to use the Last.fm API for fetching album art, refer to the Last.fm API documentation [here](https://www.last.fm/api).