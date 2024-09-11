'''
main.py

This module fetches the currently playing album art using the Last.fm API
and displays it on an LED matrix panel. It handles the configuration, 
requests the album data, and processes image URLs for display.
'''

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
    LOG_FILENAME,
)

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    level=logging.DEBUG,
        handlers=[
        logging.FileHandler(LOG_FILENAME),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class Config:
    '''
    Configuration class for fetching environment variables and setting API details.

    This class loads environment variables from a .env file and sets
    the Last.fm user and URL for API requests, along with the image
    conversion mode.

    Attributes:
        lastfm_user (str): The Last.fm username to fetch recent tracks for.
        lastfm_url (str): The URL template for the Last.fm API to get recent tracks.
        convert_mode (str): The conversion mode for images.
    '''
    def __init__(self):
        load_dotenv()
        self.lastfm_user = os.getenv('LASTFM_USER')
        self.lastfm_url = 'http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks'
        self.convert_mode = 'RGB'
        self.unknown_image_url = 'https://lastfm.freetls.fastly.net/i/u/300x300/2a96cbd8b46e442fc41c2b86b821562f.png'


def fetch_recent_track(config):
    '''
    Fetches the url of the album art corresponding with the current or most recent track scrobbled to Last.fm.

    Returns:
        str: URL of the album art image.
    ''' 
    try:
        logger.debug('Requesting recent tracks from Last.fm')
        response = requests.get(
            f'{config.lastfm_url}&user={config.lastfm_user}&api_key={LASTFM_PUBLIC_API_KEY}&format=json',
            timeout=REQUEST_TIMEOUT_S,
        )

        response.raise_for_status()
        obj = response.json()
        image_url_api = (
            obj.get('recenttracks', {})
            .get('track', [])[0]
            .get('image', [None, None, None, None])[3]['#text']
        )

        return image_url_api

    except RequestException as e:
        logger.error('HTTP Request failed: %s', e)
    except (KeyError, IndexError, TypeError) as e:
        logger.error('Error processing JSON response: %s', e)
    except json.JSONDecodeError as e:
        logger.error('Failed to decode JSON: %s', e)

    return None


def fetch_image(image_url):
    '''
    Fetches the image from the given URL.

    Args:
        image_url (str): URL of the image.

    Returns:
        PIL.Image: The image fetched.
    '''
    try:
        logger.info('Fetching image from URL: %s', image_url)
        response = requests.get(image_url, timeout=REQUEST_TIMEOUT_S)
        response.raise_for_status()
        image = Image.open(io.BytesIO(response.content))
        return image

    except RequestException as e:
        logger.error('HTTP Request for image failed: %s', e)
    except OSError as e:
        logger.error('Image opening failed: %s', e)

    return None


def save_image(image):
    '''
    Resizes and converts the given image and saves it to the board.

    Args:
        image (PIL.Image): The image to save.
    '''
    try:
        logger.info('Saving image to board')
        image = image.resize((MATRIX_WIDTH, MATRIX_HEIGHT)).convert(Config().convert_mode)
        image.save(
            os.path.join(BOARD_DRIVE_LETTER + ':', OUTPUT_IMAGE),
            OUTPUT_IMAGE.rsplit('.', maxsplit=1)[-1],
        )
    except (OSError, IOError) as e:
        logger.error('File operation failed: %s', e)


def main():
    '''
    Fetches the currently playing album art from Last.fm and saves it
    to the specified drive. The function periodically checks for updates
    in the currently playing track, retrieves the corresponding album art,
    and saves it for display.

    This function runs indefinitely until manually stopped.
    '''
    config = Config()
    image_url = ''

    while True:
        logger.debug('Sleeping for %d seconds', LOOP_SLEEP_S)
        time.sleep(LOOP_SLEEP_S)

        new_image_url = fetch_recent_track(config)
        if new_image_url and new_image_url != image_url:
            if new_image_url == config.unknown_image_url:
                logger.debug('Last.fm returned unknown image; skipping')
                continue
            image_url = new_image_url
            image = fetch_image(image_url)
            if image:
                save_image(image)
            else:
                logger.warning('Failed to fetch new image; image object empty')


if __name__ == '__main__':
    main()
