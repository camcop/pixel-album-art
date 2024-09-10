import os
import shutil
import requests
from dotenv import load_dotenv
import time
import logging
from PIL import Image
import io
from config import (
    OUTPUT_IMAGE,
    BOARD_DRIVE_LETTER,
    LASTFM_PUBLIC_API_KEY,
    LOOP_SLEEP_S,
    REQUEST_TIMEOUT_S,
    MATRIX_WIDTH,
    MATRIX_HEIGHT,
)
    
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()
LASTFM_USER = os.getenv('LASTFM_USER')
LASTFM_URL = 'http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks'
CONVERT_MODE = 'RGB'

def main():

    image_url = ''
    while True:

        logger.debug('sleeping')
        time.sleep(LOOP_SLEEP_S)

        try:
            logger.debug('requesting')
            response = requests.get(f'{LASTFM_URL}&user={LASTFM_USER}&api_key={LASTFM_PUBLIC_API_KEY}&format=json', timeout=REQUEST_TIMEOUT_S)
        except Exception as e:
            logger.error(e)
            continue

        if response.status_code != 200:
            continue
        
        try:
            obj = response.json()
            image_url_api = obj.get('recenttracks', {}).get('track', [])[0].get('image', [None, None, None, None])[3]['#text']
            logger.debug(f'{image_url_api=}')
        except Exception as e:
            logger.error(e)
            continue

        if image_url_api == image_url:
            logger.debug('image hasnt changed')
            continue
        else:
            image_url = image_url_api

        try:
            response = requests.get(image_url, timeout=REQUEST_TIMEOUT_S)
        except Exception as e:
            logger.error(e)
            continue

        if response.status_code != 200:
            logger.error(e)
            continue
        
        try:
            image = Image.open(io.BytesIO(response.content))
            image = image.resize((MATRIX_WIDTH, MATRIX_HEIGHT)).convert(CONVERT_MODE)
            image.save(os.path.join(BOARD_DRIVE_LETTER + ':', OUTPUT_IMAGE), OUTPUT_IMAGE.split('.')[-1])
        except Exception as e:
            logger.error(e)
            logger.debug(response.content)
            continue

main()