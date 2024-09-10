# README

## Overview

Dynamically display the currently playing album art on an LED matrix panel. This project integrates with Last.fm to fetch the album art and handles image format conversion, resizing, and uploading to the board.

## Key Features

- **Service Agnostic**: Compatible with any music service that scrobbles to Last.fm.
- **Public API Use**: No sign-up needed; the project utilizes a public API key provided in the code.
- **Responsible API Use**: Only polls the API every 10 seconds by default and does not pull the album art if it has not changed.

## Hardware

- [Interstate75](https://thepihut.com/products/interstate-75)
- [RGB Full-Colour LED Matrix Panel - 2mm Pitch, 64x64 Pixels](https://thepihut.com/products/rgb-full-colour-led-matrix-panel-2mm-pitch-64x64-pixels)

## Hardware setup

1. Follow [Pimoronmi's guide](https://learn.pimoroni.com/article/getting-started-with-interstate-75#introduction) to attach the LED matrix panel to the Interstate75

2. Install [CircuitPython](https://circuitpython.org/board/pimoroni_interstate75/) (tested with 9.1.3) on the Interstate75, following the guide from [Pimoroni](https://learn.pimoroni.com/article/getting-started-with-interstate-75#circuitpython)

## Installation

1. To set up the project, ensure you have Python installed and use the following command to install the required packages:

```bash
pip install -r requirements.txt
```

2. Copy `code.py` from the `interstate75` folder of the project to the root of the drive (CIRCUITPY). This code will run every time the board boots

3. Press `RST` button on the board to restart

## Configuration

Before running the application, create a file called .env at the root of the project with the following variable:

```
LASTFM_USER=your_lastfm_username
```

Then update the drive letter of the board in config.py, e.g.:

```python
BOARD_DRIVE_LETTER = 'D'
```

The image will be saved on the board under `OUTPUT_IMAGE`. If you change teh value of this variable in config.py, make sure to update the variable in `code.py` as well before copying it to the board.

## Usage

To start the application, run the main script:

```bash
python main.py
```

## Dependencies

The project relies on a few external libraries, listed in `requirements.txt`:

- `Pillow` for image processing
- `python-dotenv` for environment variable management
- `Requests` for making HTTP requests

## Inspiration and resources

This project incorporate code from the [lastfm-user-data-api](https://github.com/hankhank10/lastfm-user-data-api/tree/master) project by hankhank10.

This project was inspired by my previous project NowPlaying (which displays the currently playing track on a Waveshare e-ink display), as well as a [similar project on reddit](https://www.reddit.com/r/raspberry_pi/comments/ziz4hk/my_64x64_rgb_led_matrix_album_art_display_pi_3b/).

To understand how to use the Last.fm API for fetching album art, refer to the [Last.fm API documentation](https://www.last.fm/api).