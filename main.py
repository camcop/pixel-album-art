import os
import logging
import time
import requests

from dotenv import load_dotenv
from unidecode import unidecode

from config import BOARD_DRIVE_LETTER, IMAGE_DIR, INPUT_IMAGE, OUTPUT_IMAGE, LASTFM_PUBLIC_API_KEY, LOOP_SLEEP_S
from convert import convert, resize
from write_to_board import copy_file, create_or_update_log
from download import download_cover, fetch_last_played

load_dotenv()

LASTFM_USER = os.getenv('LASTFM_USER')
output_filename = ''

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

def main():
    initial_iteration = True
    lastplayed_album = ''
    lastplayed_artist = ''
    current_art = ''
    lastfm_session = requests.Session()
    image_session = requests.Session()

    while True:
        if not initial_iteration:
            logger.debug(f'Sleeping for {LOOP_SLEEP_S} seconds')
            time.sleep(LOOP_SLEEP_S)
        initial_iteration = False

        try:
            lastplayed_trackname, lastplayed_artist, lastplayed_album, lastplayed_image_url = fetch_last_played(lastfm_session, LASTFM_PUBLIC_API_KEY, LASTFM_USER)
            logger.info(f'Last played: "{lastplayed_trackname}" by "{lastplayed_artist}" from "{lastplayed_album}"')
            logger.info(f'Last played image URL: {lastplayed_image_url}')

        except Exception as e:
            logger.error(f'Error fetching last played track: {e}')
            continue

        if lastplayed_image_url is None:
            logger.warning('No album or artist found; skipping to the next iteration')
            continue
        
        # Remove unsafe characters from album and artist names
        remove_chars = str.maketrans('', '', r' /\\:*?"<>|')
        lastplayed_album_cleaned = unidecode(lastplayed_album).translate(remove_chars)
        lastplayed_artist_cleaned = unidecode(lastplayed_artist).translate(remove_chars)
        output_filename = f'{lastplayed_album_cleaned}-by-{lastplayed_artist_cleaned}.jpeg'

        if lastplayed_album_cleaned != current_art:
            logger.info(f'New album detected: {lastplayed_album_cleaned}. Downloading album art...')
            try:
                downloaded_file = download_cover(image_session, lastplayed_image_url, output_filename)
                logger.info(f'Successfully downloaded cover art: {downloaded_file}')
            except Exception as e:
                logger.error(f'Failed to download album art: {e}')
                continue
            current_art = lastplayed_album_cleaned

            try:
                resized_file = resize(output_filename, 64, 64)
                converted_file = convert(resized_file, 'bmp')
                copy_file(os.path.join(IMAGE_DIR, converted_file), OUTPUT_IMAGE)
                create_or_update_log(output_filename)
                logger.debug(f'Processed and updated board with new image: {converted_file}')
            except Exception as e:
                logger.error(f'Error in processing images: {e}')
        else:
            logger.debug('No new album detected; continuing loop')


if __name__ == '__main__':
    main()
