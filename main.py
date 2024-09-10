"""
main.py

This module fetches the currently playing album art using the Last.fm API
and displays it on an LED matrix panel. It handles the configuration, 
requests the album data, and processes image URLs for display.
"""

import os
import time
import logging
import io
import json
import requests
from requests.exceptions import RequestException
from dotenv import load_dotenv
from PIL import Image
from config import (
    OUTPUT_IMAGE,
    BOARD_DRIVE_LETTER,
    LASTFM_PUBLIC_API_KEY,
    LOOP_SLEEP_S,
    REQUEST_TIMEOUT_S,
    MATRIX_WIDTH,
    MATRIX_HEIGHT,
)

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s", level=logging.DEBUG
)
logger = logging.getLogger(__name__)

load_dotenv()
LASTFM_USER = os.getenv("LASTFM_USER")
LASTFM_URL = "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks"
CONVERT_MODE = "RGB"


def main():
    """
    Fetches the currently playing album art from Last.fm and displays it
    on an LED matrix panel. The function periodically checks for updates
    in the currently playing track, retrieves the corresponding album art,
    and saves it for display.

    This function runs indefinitely until manually stopped.
    """

    image_url = ""
    while True:

        logger.debug("sleeping")
        time.sleep(LOOP_SLEEP_S)

        try:
            logger.debug("requesting")
            response = requests.get(
                f"{LASTFM_URL}&user={LASTFM_USER}&api_key={LASTFM_PUBLIC_API_KEY}&format=json",
                timeout=REQUEST_TIMEOUT_S,
            )
        except RequestException as e:
            logger.error(e)
            continue

        if response.status_code != 200:
            continue

        try:
            obj = response.json()
            image_url_api = (
                obj.get("recenttracks", {})
                .get("track", [])[0]
                .get("image", [None, None, None, None])[3]["#text"]
            )
            logger.debug("%s", image_url_api)  # Changed line
        except (KeyError, IndexError) as e:  # Catching specific exceptions
            logger.error(e)
            continue
        except json.JSONDecodeError as e:  # Handle JSON decoding issues separately
            logger.error("Failed to decode JSON: %s", e)
            continue

        if image_url_api == image_url:
            logger.debug("image hasn't changed")
            continue
        else:
            image_url = image_url_api

        try:
            response = requests.get(image_url, timeout=REQUEST_TIMEOUT_S)
        except RequestException as e:
            logger.error(e)
            continue

        if response.status_code != 200:
            logger.error(e)
            continue

        try:
            image = Image.open(io.BytesIO(response.content))
            image = image.resize((MATRIX_WIDTH, MATRIX_HEIGHT)).convert(CONVERT_MODE)
            image.save(
                os.path.join(BOARD_DRIVE_LETTER + ":", OUTPUT_IMAGE),
                OUTPUT_IMAGE.rsplit(".", maxsplit=1)[-1],
            )
        except (OSError, IOError) as e:  # Catching specific exceptions
            logger.error("File operation failed: %s", e)
            logger.debug(response.content)
            continue

if __name__ == "__main__":
    main()
